import unittest
from itertools import combinations
from tqdm import tqdm
from functools import reduce
from qumin import entropy

class DistributionTest(unittest.TestCase):

    def test_slow_calc_n(self, distribution, n):
        r"""Test with slow distribution"""

        patterns = distribution.patterns
        classes = distribution.classes
        columns = list(distribution.paradigms.columns)

        pat_order = {}
        for a, b in patterns:
            pat_order[(a, b)] = (a, b)
            pat_order[(b, a)] = (a, b)

        indexes = list(combinations(columns, n))

        rows = []
        for predictors in tqdm(indexes):
            #  combinations gives us all x, y unordered unique pair for all of
            # the n predictors.
            pairs_of_predictors = list(combinations(predictors, 2))

            predsselector = reduce(lambda x, y: x & y,
                                   (distribution.hasforms[x] for x in predictors))

            for out in (x for x in columns if x not in predictors):


                selector = predsselector & distribution.hasforms[out]

                # Getting intersection of patterns events for each predictor:
                # x~z, y~z
                A = patterns.loc[selector, [pat_order[(pred, out)] for pred in predictors]]

                # Known classes Class(x), Class(y) and known patterns x~y
                known_classes = classes.loc[selector, [(pred, out) for pred in predictors]]
                known_patterns = patterns.loc[selector, pairs_of_predictors]

                B = known_classes + known_patterns

                if distribution.features is not None:
                    B = B + distribution.features[selector]

                cond_events = A.groupby(B, sort=False)
                classes_p = entropy.P(B)
                cond_p = entropy.P(cond_events)
                surprisal = cond_p.groupby(level=0).apply(entropy.entropy)
                slow_ent = (classes_p * surprisal).sum()
                rows.append([predictors, out, slow_ent])

        ############ TODO: MOVE TESTING OF EQUALITY TO TESTS ! ########################""
        ### TODO: rows => data => self.data
        ### Then compare
        ## TODO: strategy


    def test_slow_calc_1(self, distrib):
        """Print a log of the probability distribution for one predictor.

        Writes down the distributions
        :math:`P( patterns_{c1, c2} | classes_{c1, c2} )`
        for all unordered combinations of two column
        names in :attr:`PatternDistribution.paradigms`.
        Also writes the entropy of the distributions.

        Arguments:
            sanity_check (bool): Use a slower calculation to check that the results are exact.
        """

        patterns = distrib.patterns.map(lambda x: x[0])
        rows = []

        for column in patterns:
            for pred, out in [column, column[::-1]]:
                selector = distrib.hasforms[pred] & distrib.hasforms[out]

                A = patterns.loc[selector, :][column]
                B = distrib.add_features(distrib.classes.loc[selector, :][(pred, out)])
                cond_events = A.groupby(B, sort=False)

                classes_p = entropy.P(B)
                cond_p = entropy.P(cond_events)

                surprisal = cond_p.groupby(level=0).apply(entropy)
                slow_ent = (classes_p * surprisal).sum()
                rows.append([pred, out, slow_ent])
        ### TODO: move to tests the sanity check
        # TODO: rows => dataframe => self.data


    def value_check(self, n):
        """Check that predicting from n predictors isn't harder than with less.

        TODO: Move this to tests !!

        Check that the value of entropy from n predictors c1, ....cn
        is lower than the entropy from n-1 predictors c1, ..., cn-1
        (for all computed n preds entropies).

        Arguments:
            n: number of predictors.
        """
        if self.data[1] is None or self.data[n] is None:
            return None

        log.info("Now checking if all entropies with n predictors "
                 "are lower than their counterparts with n-1 predictors.")

        found_wrong = False

        entropies_n = self.data[n]
        entropies_one = self.data[1]

        for predictors in entropies_n.index:

            for out in entropies_n:
                value_n = entropies_n.at[predictors, out]

                for predictor in predictors:
                    value_one = entropies_one.at[predictor, out]

                    if value_n > value_one and \
                            abs(value_n - value_one) > 1e-5:
                        found_wrong = True
                        log.debug("Found error: H({} → {}) = {}"
                                  "(type = {}) "
                                  " higher than H({} → {}) = {} "
                                  " (type= {})"
                                  "".format(", ".join(predictors),
                                            out,
                                            value_n,
                                            type(value_n),
                                            predictor, out,
                                            value_one,
                                            type(value_one)))

        if found_wrong:
            log.warning("Found errors ! Check logfile or re-run with -d for details.")
        else:
            log.info("Everything is right !")

        return found_wrong