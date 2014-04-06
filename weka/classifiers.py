# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# classifiers.py
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

import javabridge
import os
import sys
import getopt
import core.jvm as jvm
import core.classes as classes
from core.classes import WekaObject
from core.classes import OptionHandler
from core.converters import Loader

class Classifier(OptionHandler):
    """
    Wrapper class for classifiers.
    """
    
    def __init__(self, classname):
        """ Initializes the specified classifier. """
        jobject = Classifier.new_instance(classname)
        self._enforce_type(jobject, "weka.classifiers.Classifier")
        super(Classifier, self).__init__(jobject)
        
    def build_classifier(self, data):
        """ Builds the classifier with the data. """
        javabridge.call(self.jobject, "buildClassifier", "(Lweka/core/Instances;)V", data.jobject)
        
    def classify_instance(self, inst):
        """ Peforms a prediction. """
        return javabridge.call(self.jobject, "classifyInstance", "(Lweka/core/Instance;)V", data.jobject)
        
    def distribution_for_instance(self, inst):
        """ Peforms a prediction, returning the class distribution. """
        pred = javabridge.call(self.jobject, "distributionForInstance", "(Lweka/core/Instance;)V", data.jobject)
        return jvm.ENV.get_double_array_elements(pred)


class Evaluation(WekaObject):
    """
    Evaluation class for classifiers. 
    """
    
    def __init__(self):
        """ Initializes an Evaluation object. """
        super(Evaluation, self).__init__(Evaluation.new_instance("weka.classifiers.Evaluation"))
        
    @classmethod
    def evaluateModel(self, classifier, args):
        """ Evaluates the classifier with the given options. """
        return javabridge.static_call("Lweka/classifiers/Evaluation;", "evaluateModel", "(Lweka/classifiers/Classifier;[Ljava/lang/String;)Ljava/lang/String;", classifier.jobject, args)

def main(args):
    """
    Runs a filter from the command-line. Calls JVM start/stop automatically.
    Options:
        -j jar1[:jar2...]
        -t train
        [-T test]
        [-c classindex]
        [-d output model file]
        [-l input model file]
        [-x num folds]
        [-s seed]
        [-v # no stats for training]
        [-o # only stats, no model]
        [-i # information-retrieval stats per class]
        [-k # information-theoretic stats]
        [-m cost matrix file]
        [-g graph file]
        classifier classname
        [classifier options]
    """

    usage = "Usage: weka.classifiers -l jar1[" + os.pathsep + "jar2...] -t train [-T test] [-c classindex] [-d output model file] [-l input model file] [-x num folds] [-s seed] [-v # no stats for training] [-o # only stats, no model] [-i # information-retrieval stats per class] -kl # information-theoretic stats] [-m cost matrix file] [-g graph file] classifier classname [classifier options]"
    optlist, args = getopt.getopt(args, "j:t:T:c:d:l:x:s:voikm:g:")
    if len(args) == 0:
        raise Exception("No clusterer classname provided!\n" + usage)
    for opt in optlist:
        if opt[0] == "-h":
            print(usage)
            return
        
    jars    = []
    params  = []
    train   = None
    for opt in optlist:
        if opt[0] == "-j":
            jars = opt[1].split(os.pathsep)
        elif opt[0] == "-t":
            params.append(opt[0])
            params.append(opt[1])
            train = opt[1]
        elif opt[0] == "-T":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-d":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-l":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-x":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-s":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-v":
            params.append(opt[0])
        elif opt[0] == "-o":
            params.append(opt[0])
        elif opt[0] == "-i":
            params.append(opt[0])
        elif opt[0] == "-k":
            params.append(opt[0])
        elif opt[0] == "-m":
            params.append(opt[0])
            params.append(opt[1])
        elif opt[0] == "-g":
            params.append(opt[0])
            params.append(opt[1])
        
    # check parameters
    if train == None:
        raise Exception("No train file provided ('-t ...')!")
        
    jvm.start(jars)
    try:
        classifier = Classifier(args[0])
        args = args[1:]
        if len(args) > 0:
            classifier.set_options(args)
        print(Evaluation.evaluateModel(classifier, params))
    except Exception, e:
        print(e)
    finally:
        jvm.stop()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception, e:
        print(e)
