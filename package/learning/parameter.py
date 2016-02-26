#!/usr/local/bin/python2.7
# -*-coding:UTF-8-sig -*-

"""
    Module for executing calculation about parameters
    Learning Algorithm - 2015 - Subena
"""

from compiler.ast import flatten
import itertools

from sqlalchemy.sql.functions import func

from base import DBSession, logging
import numpy as np
from package.model.tables import Criterion, Value, Stats,Alerts

session = DBSession()
criteria = session.query(Criterion).all()

def execute():
    logging.info( "\nStart learning parameters..." )
    
    #calcul all proba dependencies according to proba and their parenthood
    getProbaForAllMeasures()
    
def getAlertsFromStats():
    """
        Get alerts from calculated stats (see getProbaForAllMeasures)
        for each stat if a pattern does not correspond then create an alert
    """
    
    stats = None
    #get stats with stats parent and children associations splitted in two parts
    stats = session.query(Stats).all()
    #get measures from database grouped by timestamp
    measures = getAllMeasures()
        
    ialert = 0;    
    alerts = list()
    
    logging.info( "Alerts detection starts..." )
    logging.info( "Delete all previous calculated alerts" )
    
    #remove all
    session.query(Alerts).delete()
    session.commit() 
    
    alertProbaLimit = 0.2
    logging.info( "Max probability detection : %s",alertProbaLimit )
    
    for measure in measures:
        #stats inf to a limit
        for stat in [s for s in stats if s.proba < alertProbaLimit]:
            idsStat = np.array(stat.association.split(';'),dtype=int) - 1
            #si une valeur est trouvée
            if (stat.value.split(';') == measure[1][idsStat]).all():
                ialert += 1
                source = str(idsStat[0] + 1) + ";" + str(measure[1][idsStat[0]])
                #create alert
                alerts.append(Alerts(id=ialert,timestamp=measure[0],source=source,action=0,risk=stat.proba))
    
    #save stats
    session.add_all(alerts)
    session.commit()
    
    if len(stats) > 0:
        logging.info( "%s alerts have been detected from %s measures",format( len(alerts) ),format( len(measures) ) )
    else:
        logging.info( "None alert detected" )
    
def getProbaForLastMeasures(numberOfLastMeasures):
    """
        Get last measure from database and calculate probabilities
        numberOfLastValues specifies how many measures should be considered in calculation
    """
    
    measures = getAllMeasures()
    #remove timestamp from measures
    measures = measures[:,1:]
    measures = np.array([list(m) for m in measures],dtype=object)
    measures = np.reshape(measures, (measures.shape[0],measures.shape[2]))
    
    #set numberOfLastMeasures to max if param equals 0
    if numberOfLastMeasures == 0:
        numberOfLastMeasures = measures.shape[0]
    
    logging.info( "Calculate proba of the last %s measures... ",format(numberOfLastMeasures) )
    
    if(len(measures) == 0):
        logging.warning( "No values are available for learning" )
    else:
            
        #get only required measures
        measuresToEvaluate = measures[:numberOfLastMeasures]
        
        #variable where proba result will be stored
        result = np.ones(len(measuresToEvaluate))
                                    
        for c in criteria:
            if(len(c.values) > 0):
                
                idsParent = []
                #if criterion has one or more parents          
                if(len(c.parents) > 0):
                    sortParents = sorted(c.parents, key=lambda p: p.id)
                    idsParent = [p.id for p in sortParents]
                    ids = list(np.array(idsParent) - 1)
                    
                    #init num with value of criterion
                    truncation = np.ones((len(measuresToEvaluate),len(c.parents) + 1),dtype=object)
                    index = 0
                    truncation[:,index] = measuresToEvaluate[:,c.id - 1]
                                
                    for p in c.parents:
                        index += 1
                        truncation[:,index] = measuresToEvaluate[:,p.id - 1]
                                                                                                                                                                    
                    #for each combination of category, calculation is done for denominator
                    den = np.array([np.count_nonzero([(t == m).all() for m in measures[:,ids]]) for t in truncation[:,1:]])
                    #for each combination of category, calculation is done for numerator
                    num = np.array([np.count_nonzero([(t == m).all() for m in measures[:,[c.id - 1,] + ids]]) for t in truncation])
                    
                    #set num = 0 and den = 1 for avoiding division by zero and getting a result
                    num[np.where(den == 0)] = 0;
                    den[np.where(den == 0)] = 1;
                                                                      
                #if there is no parent for this criterion  
                else:
                    #den is total number of values for this criteria
                    den = len(measures)
                    #for each combination of category, calculation is done for numerator
                    num = np.array([np.count_nonzero([m == mte for mte in measures[:,c.id - 1]]) for m in measuresToEvaluate[:,c.id - 1]])

                #result is calculated by multiplying previous value with current proba
                result = np.multiply(result,np.divide(num,den,dtype=float))
                                                    
        logging.info( "Final proba for last measures :\n%s",result ) 
        
        return result   
                 
def getProbaForAllMeasures():
    """
        Algorithm for calculating conditional probabilities for all categories in all measures
    """
    
    logging.info( "Calculate all conditionnal probabilities" )
    istats = 0
    
    measures = getAllMeasures()
    measures = measures[:,1:]
    measures = np.array([list(m) for m in measures],dtype=object)
    measures = np.reshape(measures, (measures.shape[0],measures.shape[2]))
    
    if(len(measures) == 0):
        logging.info( "No values are available for learning" )
    else:
        
        logging.info( "Delete all previous calculated stats" )
        #first, remove all
        session.query(Stats).delete()
        session.commit()
            
        #loop through criteria
        for c in criteria:
            logging.info( "\nCriterion id : %s",format(c.id) )

            if len(c.values) == 0:
                continue
            
            stats = list()
            
            #if criterion has one or more parents
            if(len(c.parents) > 0):
                sortParents = sorted(c.parents, key=lambda p: p.id)
                ids = [str(c.id),] + [str(sp.id) for sp in sortParents]
                catChild = list(set([v.category for v in c.values]))
                catParent = [flatten(set([str(upc.category) for upc in p.values])) for p in sortParents]
                catChildAndParent = [catChild,] + catParent
        
                productNumerator = list(itertools.product(*catChildAndParent))
                
                #reshape combinationCatParents in a matrix [values number,parent number]
                #catNumerator = np.reshape(productNumerator, [len(productNumerator),len(c.parents) + 1])
                catNumerator = np.array(productNumerator)
                                
                if len(catNumerator) > 0:

                    catDenominator = catNumerator[:,1:]
                                                
                    #index for truncation measures matrix
                    index = 0
                    #init truncation matrix with 0
                    truncation = ()
                    truncation = np.zeros((measures.shape[0],len(c.parents) + 1),dtype=object)
                                                            
                    #truncate measures with only current criterion and parent columns
                    truncation[:,index] = measures[:,c.id - 1]
                                        
                    for p in c.parents:
                        index += 1
                        truncation[:,index] = measures[:,p.id - 1]
                                       
                    #for each combination of category, calculation is done for denominator
                    den = [np.count_nonzero([(cd == t).all() for t in truncation[:,1:]]) for cd in catDenominator]
                    #for each combination of category, calculation is done for numerator
                    num = [np.count_nonzero([(cn == t).all() for t in truncation]) for cn in catNumerator]       
                        
                    #for avoiding to divide by 0
                    num = np.take(num,np.nonzero(den))
                    #get categories of parents
                    productNumerator = [productNumerator[i] for i in list(np.nonzero(den)[0])]
                    den = np.take(den,np.nonzero(den))
                    
                    results = np.divide(num,den,dtype=float)
                    
                    #persist stats to db
                    for i in range(0,len(productNumerator)):
                        istats += 1
                        listProduct = list(productNumerator[i])
                        stats.append(Stats(id=istats,association=';'.join(ids),parent=';'.join(listProduct[:1]),children=';'.join(listProduct[1:]),value=';'.join(listProduct),proba=results[0][i]))
                    
                    session.add_all(stats)
                    session.commit()
                    
                    logging.info( "Criteria : %s",format(ids) )
                    logging.info( "Categories : %s",format(productNumerator) )
                    logging.info( "Proba : %s",format(results[0]) )
        
                else:
                    logging.warning( 'No measure available for this criterion and/or parents' )
                    
            #if there is no parent for this criterion
            else:
                logging.warning( 'No relationship find for criterion id : %s',format(c.id) )
                #TODO useless?
                #catChild = np.array(list(set([v.category for v in c.values])))            
                #print [np.count_nonzero([(m == cc).all() for cc in catChild]) for m in measures]
                
    if istats > 0:
        print 'SUCCESS: {} stats have been calculated and inserted in database'.format(istats) 

def getAllMeasures():
    """
        Method for getting all measures from database with timestamp
        TODO - an other complex function would improve this by evaluating missing values
    """
    
    logging.info( "Get all measure from database" )
    
    #select t,count(idCriterion) as count from value group by(t) having count > 7;
    measures = None
    measures = session.query(Value.timestamp,func.group_concat(Value.category.op('order by')(Value.criterion_id))).group_by(Value.timestamp)
    criteriaWithValues = [c for c in criteria if len(c.values) > 0]
    #don't keep value with too many or less values
    #a future learning algo will calculate missing values
    measures = [[m[0],np.array(m[1].split(','),dtype=object)] for m in list(measures) if len(m[1].split(',')) == len(criteriaWithValues)]
    measures = np.array(measures,dtype=object)
    
    return np.array(measures,dtype=object)

            
                