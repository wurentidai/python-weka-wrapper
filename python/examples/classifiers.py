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

import os
import weka.core.jvm as jvm
import examples.helper as helper
from weka.core.converters import Loader
from weka.classifiers import Classifier
from weka.classifiers import Evaluation
from weka.core.classes import Random
import weka.plot.classifiers as plot_cls


def main():
    """
    Just runs some example code.
    """

    # load a dataset
    iris_file = helper.get_data_dir() + os.sep + "iris.arff"
    helper.print_info("Loading dataset: " + iris_file)
    loader = Loader("weka.core.converters.ArffLoader")
    iris_data = loader.load_file(iris_file)
    iris_data.set_class_index(iris_data.num_attributes() - 1)

    # build a classifier and output model
    helper.print_title("Training J48 classifier on iris")
    classifier = Classifier("weka.classifiers.trees.J48")
    classifier.set_options(["-C", "0.3"])
    classifier.build_classifier(iris_data)
    print(classifier)
    print(classifier.graph())
    plot_cls.plot_dot_graph(classifier.graph())

    # cross-validate nominal classifier
    helper.print_title("Cross-validating SMO on iris")
    classifier = Classifier("weka.classifiers.functions.SMO")
    classifier.set_options(["-M"])
    evaluation = Evaluation(iris_data)
    evaluation.crossvalidate_model(classifier, iris_data, 10, Random(42))
    print(evaluation.to_summary())
    print(evaluation.to_class_details())
    print(evaluation.to_matrix())
    print("areaUnderPRC/0: " + str(evaluation.area_under_prc(0)))
    print("weightedAreaUnderPRC: " + str(evaluation.weighted_area_under_prc()))
    print("areaUnderROC/1: " + str(evaluation.area_under_roc(1)))
    print("weightedAreaUnderROC: " + str(evaluation.weighted_area_under_roc()))
    print("avgCost: " + str(evaluation.avg_cost()))
    print("totalCost: " + str(evaluation.total_cost()))
    print("confusionMatrix: " + str(evaluation.confusion_matrix()))
    print("correct: " + str(evaluation.correct()))
    print("pctCorrect: " + str(evaluation.percent_correct()))
    print("incorrect: " + str(evaluation.incorrect()))
    print("pctIncorrect: " + str(evaluation.percent_incorrect()))
    print("unclassified: " + str(evaluation.unclassified()))
    print("pctUnclassified: " + str(evaluation.percent_unclassified()))
    print("coverageOfTestCasesByPredictedRegions: " + str(evaluation.coverage_of_test_cases_by_predicted_regions()))
    print("sizeOfPredictedRegions: " + str(evaluation.size_of_predicted_regions()))
    print("falseNegativeRate: " + str(evaluation.false_negative_rate(1)))
    print("weightedFalseNegativeRate: " + str(evaluation.weighted_false_negative_rate()))
    print("numFalseNegatives: " + str(evaluation.num_false_negatives(1)))
    print("trueNegativeRate: " + str(evaluation.true_negative_rate(1)))
    print("weightedTrueNegativeRate: " + str(evaluation.weighted_true_negative_rate()))
    print("numTrueNegatives: " + str(evaluation.num_true_negatives(1)))
    print("falsePositiveRate: " + str(evaluation.false_positive_rate(1)))
    print("weightedFalsePositiveRate: " + str(evaluation.weighted_false_positive_rate()))
    print("numFalsePositives: " + str(evaluation.num_false_positives(1)))
    print("truePositiveRate: " + str(evaluation.true_positive_rate(1)))
    print("weightedTruePositiveRate: " + str(evaluation.weighted_true_positive_rate()))
    print("numTruePositives: " + str(evaluation.num_true_positives(1)))
    print("fMeasure: " + str(evaluation.f_measure(1)))
    print("weightedFMeasure: " + str(evaluation.weighted_f_measure()))
    print("unweightedMacroFmeasure: " + str(evaluation.unweighted_macro_f_measure()))
    print("unweightedMicroFmeasure: " + str(evaluation.unweighted_micro_f_measure()))
    print("precision: " + str(evaluation.precision(1)))
    print("weightedPrecision: " + str(evaluation.weighted_precision()))
    print("recall: " + str(evaluation.recall(1)))
    print("weightedRecall: " + str(evaluation.weighted_recall()))
    print("kappa: " + str(evaluation.kappa()))
    print("KBInformation: " + str(evaluation.kb_information()))
    print("KBMeanInformation: " + str(evaluation.kb_mean_information()))
    print("KBRelativeInformation: " + str(evaluation.kb_relative_information()))
    print("SFEntropyGain: " + str(evaluation.sf_entropy_gain()))
    print("SFMeanEntropyGain: " + str(evaluation.sf_mean_entropy_gain()))
    print("SFMeanPriorEntropy: " + str(evaluation.sf_mean_prior_entropy()))
    print("SFMeanSchemeEntropy: " + str(evaluation.sf_mean_scheme_entropy()))
    print("matthewsCorrelationCoefficient: " + str(evaluation.matthews_correlation_coefficient(1)))
    print("weightedMatthewsCorrelation: " + str(evaluation.weighted_matthews_correlation()))
    print("class priors: " + str(evaluation.get_class_priors()))
    print("numInstances: " + str(evaluation.num_instances()))
    print("meanAbsoluteError: " + str(evaluation.mean_absolute_error()))
    print("meanPriorAbsoluteError: " + str(evaluation.mean_prior_absolute_error()))
    print("relativeAbsoluteError: " + str(evaluation.relative_absolute_error()))
    print("rootMeanSquaredError: " + str(evaluation.root_mean_squared_error()))
    print("rootMeanPriorSquaredError: " + str(evaluation.root_mean_prior_squared_error()))
    print("rootRelativeSquaredError: " + str(evaluation.root_relative_squared_error()))

    # load a numeric dataset
    bolts_file = helper.get_data_dir() + os.sep + "bolts.arff"
    helper.print_info("Loading dataset: " + bolts_file)
    loader = Loader("weka.core.converters.ArffLoader")
    bolts_data = loader.load_file(bolts_file)
    bolts_data.set_class_index(bolts_data.num_attributes() - 1)

    # build a classifier and output model
    helper.print_title("Training LinearRegression on bolts")
    classifier = Classifier("weka.classifiers.functions.LinearRegression")
    classifier.set_options(["-S", "1", "-C"])
    classifier.build_classifier(bolts_data)
    print(classifier)

    # cross-validate numeric classifier
    helper.print_title("Cross-validating LinearRegression on bolts")
    classifier = Classifier("weka.classifiers.functions.LinearRegression")
    classifier.set_options(["-S", "1", "-C"])
    evaluation = Evaluation(bolts_data)
    evaluation.crossvalidate_model(classifier, bolts_data, 10, Random(42))
    print(evaluation.to_summary())
    print("correlationCoefficient: " + str(evaluation.correlation_coefficient()))
    print("errorRate: " + str(evaluation.error_rate()))
    helper.print_title("Header - bolts")
    print(str(evaluation.header()))
    helper.print_title("Predictions on bolts")
    i = 0
    preds = evaluation.predictions()
    for pred in preds:
        i += 1
        print(str(i) + ": " + str(pred) + " -> error=" + str(pred.error()))
    plot_cls.plot_classifier_errors(preds, outfile="/tmp/out2.png")


if __name__ == "__main__":
    try:
        jvm.start()
        main()
    except Exception, e:
        print(e)
    finally:
        jvm.stop()
