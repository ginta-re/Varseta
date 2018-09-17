import sys

from itertools import islice

import utterances
import evaluation


def window(seq, n=2):
    """ Returns a sliding window (of width n) over data from the iterable
    s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ... """
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def matches_incremental(it, minimum_matches, return_count=True, ids=None):
    """Given an iterator returns the minimum matches."""

    matches = 0
    matches_list = []

    for count, i in enumerate(it):
        pairs = window(i)
        for k, j in pairs:
            if len(set(k).intersection(set(j))) >= minimum_matches:
                matches += 1
                if ids:
                    matches_list.append((ids[count], i))
                else:
                    matches_list.append(i)

                # stop iterating through pairs when a match is found
                break

    if return_count:
        return matches
    else:
        return matches_list


def matches_anchor(it, minimum_matches, return_count=True, ids=None):
    """Returns varation set matches using anchor method"""

    matches = 0
    matches_list = []

    for count, i in enumerate(it):
        utterances = iter(i)
        first = next(utterances)

        for utterance in utterances:
            if len(set(first).intersection(set(utterance))) >= minimum_matches:
                matches += 1
                if ids:
                    matches_list.append((ids[count], i))
                else:
                    matches_list.append(i)

    if return_count:
        return matches
    else:
        return matches_list


def convert_varseta_format(results):
    """ Returns ids and matches in the format for the Varseta evaluation

    [[[(id_1_1, id_1_2), (id_2_1, id_2_2)], ["utterance_1", "utterance_2"]], ...]
    to
    [[['id_1_1', 'id_1_2', 'Utterance_1'],['id_2_1', 'id_2_2', 'utterance_2']], ...]
    """

    return_list = []

    for result in results:
        dummy_list = []

        for id_, match_list in zip(result[0], result[1]):
            combined = list(id_)
            combined.append(' '.join(match_list))
            dummy_list.append(combined)

        return_list.append(dummy_list)

    return return_list 


def decode_args(args):
    """Parses commandline args"""

    if len(args) != 4:
        sys.exit("Please read notes.txt for command line usage")
    try:
        return args[1], int(args[2]), int(args[3])
    except:
        sys.exit("Please read notes.txt for command line usage")


def main():

    algorithm, window_eval, min_matches = decode_args(sys.argv)

    to_do = [
        ("DATA/Swedish_MINGLE_dataset/plain/1", "DATA/Swedish_MINGLE_dataset/GOLD/1")
            ]

    u = utterances.Utterances(to_do[0][0], to_do[0][1])
    gold_utterances = u._goldutterances

    utterances_reformatted = []
    ids = []

    for utterance in u._utterances:
        new_utt = utterance[2].split()
        utterances_reformatted.append(new_utt)
        ids.append((utterance[0], utterance[1]))

    utt_iter = window(utterances_reformatted, window_eval)
    id_iter = window(ids, window_eval)
    ids = [i for i in id_iter]

    if algorithm == "anch":
        ids_and_matches = matches_anchor(utt_iter, min_matches, False, ids)
    else:
        ids_and_matches = matches_incremental(utt_iter, min_matches, False, ids)

    combined = convert_varseta_format(ids_and_matches)

    e = evaluation.Evaluation(combined, gold_utterances)


if __name__ == "__main__":
    main()

