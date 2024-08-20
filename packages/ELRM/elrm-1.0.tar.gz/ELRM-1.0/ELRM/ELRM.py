import string
import pandas as pd
import math
import time
from codebleu import calc_codebleu

py_operators=['+','-','*','/','//','%','>','<','=']


def get_diff_lists(list1,list2):
    difference_result = []
    for item in list1:
        if item not in list2:
            difference_result.append(item)
    return difference_result
#
# ans_list = ["abc", "def", "aaaaaaa", "cccccccccccc"]
# gen_list = ["abc", "df", "aaaaa", "cccccccccccc"]
# def weight(gen_list, ele):
#     from collections import Counter
#     gen_rep_dict = dict(Counter(gen_list))
#     keys = list(gen_rep_dict.keys())
#     weight = 0
#     if ele in keys:
#         weight = gen_rep_dict[ele] / len(gen_list)
#     return weight

#####################################For punctuation category #########################################################

def get_sum_weights_pun(ans_list, gen_list,lambda_p,n_gram):
    avg_len_ans = get_avg_length_ngram(ans_list,n_gram)
    avg_len_gen = get_avg_length_ngram(gen_list,n_gram)
    TP_weights = []
    FP_weights = []
    FN_weights = []
    TN_weights = []


    for v1 in gen_list:
        if v1 in ans_list:  # TP
            weight=1
            TP_weights.append(weight)


        else:  # FP

            weight=1
            FP_weights.append(weight)

    for v2 in ans_list:
        if v2 not in gen_list:  # FN
            weight=1
            FN_weights.append(weight)
        else:
            TN_weights.append(1)

    sum_TP_weights = 0.4 * sum(TP_weights)
    sum_FP_weights = 0.77 * sum(FP_weights)
    sum_FN_weights = 0.7 * sum(FN_weights)

    return sum_TP_weights, sum_FP_weights, sum_FN_weights,sum(FN_weights)

def get_precision_pun(ans_list, gen_list,lambda_p,n_gram):
    sum_TP_weights, sum_FP_weights, sum_FN_weights,_ = get_sum_weights_pun(ans_list, gen_list,lambda_p,n_gram)
    precision = sum_TP_weights / (sum_TP_weights + sum_FP_weights + 1e-10)  # avoid division by zero
    return precision

def get_recall_pun(ans_list, gen_list,lambda_p,n_gram):
    sum_TP_weights, sum_FP_weights, sum_FN_weights,_ = get_sum_weights_pun(ans_list, gen_list,lambda_p,n_gram)
    recall = sum_TP_weights / (sum_TP_weights + sum_FN_weights + 1e-10)  # avoid division by zero
    return recall

###########################################For Lexicon category ####################################################
def get_weight(alpha, avg_ans_len, gen_word_len):
    numerator = alpha
    length = abs(avg_ans_len - gen_word_len)
    # length = avg_ans_len - gen_word_len
    denominator = 1 + abs(alpha - 1) * (math.exp(length))
    weight = numerator / denominator

    return weight

def get_weight_FP(alpha, avg_ans_len, gen_word_len):
    numerator = alpha
    length = gen_word_len-avg_ans_len
    denominator = 1 + abs(alpha - 1) * (math.exp(length))
    weight = numerator / denominator

    return weight


def get_avg_length_ngram(list,n_gram):
    avg_length=0
    if n_gram==1:
        num = len(list)
        total_length = 0
        for l in list:
            total_length += len(l)
        avg_length = total_length / (num++1e-10)
    else:

        length = []
        for l in list:
            one_str = ''.join(l)
            length.append(len(one_str))
        avg_length = sum(length) / (len(list)++1e-10)


    return avg_length

# get_avg_length_ngram([["a","abc"],["def","aaaaaaa"],["cccccccccccc","111111"]],1)
# get_avg_length_ngram([["a","abc"],["def","aaaaaaa"],["cccccccccccc","111111"]],2)
# get_avg_length_ngram([["a","abc","def"],["aaaaaaa","cccccccccccc","111111"]],3)

def get_len_list(g):
    length=0
    if isinstance(g,list):
        for l in g:
            length=length+len(l)
    else:
        length=len(g)

    return length

def get_sum_weights(ans_list, gen_list,alpha,n_gram):
    # ans_list = ans_dict.values()
    # gen_list = gen_dict.values()
    avg_len_ans = get_avg_length_ngram(ans_list,n_gram)
    avg_len_gen = get_avg_length_ngram(gen_list,n_gram)

    # we ignore the influence of index because the form can be access chain
    TP_weights = []
    FP_weights = []
    FN_weights = []
    TN_weights=[]
    for g in gen_list:
        len_g = get_len_list(g)
        if g in ans_list:  # TP

            weight = get_weight(7, avg_len_gen, len_g)
            TP_weights.append(weight)
        else:  # FP
            weight = get_weight(2, avg_len_gen, len_g)
            FP_weights.append(weight)

    for a in ans_list:
        len_a = len(a)
        if a not in gen_list:  # FN
            weight = get_weight(2, avg_len_gen, len_a)
            FN_weights.append(weight)
        else:
            TN_weights.append(1)

    sum_TP_weights = sum(TP_weights)
    sum_FP_weights = sum(FP_weights)
    sum_FN_weights = sum(FN_weights)


    return sum_TP_weights, sum_FP_weights, sum_FN_weights,sum(FN_weights)

def get_precision(ans_list, gen_list,alpha,n_gram):
    sum_TP_weights, sum_FP_weights, sum_FN_weights,_ = get_sum_weights(ans_list, gen_list,alpha,n_gram)
    precision = sum_TP_weights / (sum_TP_weights + sum_FP_weights + 1e-10)  # avoid division by zero
    return precision


def get_recall(ans_list, gen_list,alpha,n_gram):
    sum_TP_weights, sum_FP_weights, sum_FN_weights,_ = get_sum_weights(ans_list, gen_list,alpha,n_gram)
    recall = sum_TP_weights / (sum_TP_weights + sum_FN_weights + 1e-10)  # avoid division by zero
    return recall


def get_f_beta(beta,precision,recall):
    f_beta = ((1 + beta ** 2) * precision * recall) / (
                (beta ** 2) * precision + recall + 1e-10)  # avoid division by zero
    return f_beta


def accuracy():
    return
###################################################Iterators##################################################
def find_same_n_gram(list):
    list1=list[0:3]
    same_num=0
    for l in list:
        if l in list1:
            same_num=same_num+1
    return same_num

def get_n_gram_lists(n,elems):
    pairs=None
    if n>=len(elems):
        pairs=[elems]
    else:
        pairs = [elems[i:i+n] for i in range(len(elems) - n)]
    return pairs






def to_ordered_list(statement):
    statement=str(statement)
    statement=statement.replace('\n', '').split(" ")
    statement_list=[]
    for i in statement:
        i=str(i)
        for j in i:
            if j in string.punctuation:
                i=i.replace(j, "*" + j + "*")
        ele = i.split("*")
        ele = [i for i in ele if i != '']
        statement_list.extend(ele)

    punc=[]
    lexicon=[]
    operators=[]
    number=[]
    for p in statement_list:
        if p in py_operators and p in string.punctuation:
            operators.extend(p)
        elif p in string.punctuation:
            punc.extend(p)
        elif p.isnumeric():
            number.extend(p)
        else:
            lexicon.append(p)

    return statement_list,lexicon,punc,number,operators

def to_dict(statement):
    statement = str(statement)
    statement = statement.replace('\n', '').split(" ")
    statement_list = []
    for i in statement:
        i = str(i)
        for j in i:
            if j in string.punctuation:
                i = i.replace(j, "*" + j + "*")
        ele = i.split("*")
        ele = [i for i in ele if i != '']
        statement_list.extend(ele)

    punc = {}
    lexicon = {}
    operators = {}
    number = {}
    statement_dict={}
    index=0
    for p in statement_list:
        statement_dict[index]=p
        if p in py_operators and p in string.punctuation:
            operators[index]=p
        elif p in string.punctuation:
            punc[index]=p
        elif p.isnumeric():
            number[index]=p
        else:
            lexicon[index]=p
        index=index+1

    return statement_dict, lexicon, punc, number, operators


def convert_to_for_compare(patch, gene):
    patch=str(patch)
    gene=str(gene)
    patch_List=patch.split('\n')
    gene_list=gene.split('\n')
    if str(patch)[0]=="#":
        patch_List=patch_List[1:]

    len_p=len(patch_List)
    len_g=len(gene_list)


    if len_p-len_g>0:
        patch_List=patch_List[:len_g]

    if len_p-len_g<0:
        gene_list=gene_list[:len_p]

    patch_str= ' '.join([str(elem) for elem in patch_List])

    gen_str=' '.join([str(elem) for elem in gene_list])

    return patch_str,gen_str


def get_lex_punc_num_op_list(statement_list):
    punc = []
    lexicon = []
    operators = []
    number = []
    for p in statement_list:
        if p in py_operators and p in string.punctuation:
            operators.extend(p)
        elif p in string.punctuation:
            punc.extend(p)
        elif p.isnumeric():
            number.extend(p)
        else:
            lexicon.append(p)
    return lexicon,punc,number,operators

# def get_ELEM_n_gram(a_statement_list,g_statement_list,n_gram):
def get_ELEM(a_punc,g_punc,a_lexicon,g_lexicon,n_gram):


    g_n_gram_lexicon = get_n_gram_lists(n_gram, g_lexicon)
    g_n_gram_punc = get_n_gram_lists(n_gram, g_punc)

    a_n_gram_lexicon = get_n_gram_lists(n_gram, a_lexicon)
    a_n_gram_punc = get_n_gram_lists(n_gram, a_punc)


    alpha=3
    beta=1
    # beta=0.5
    lambda_p=0.1

    # for lexical category
    # gen_precision=get_precision(a_lexicon, g_lexicon,alpha,n_gram)
    # gen_recall=get_recall(a_lexicon, g_lexicon,alpha,n_gram)
    gen_precision = get_precision(a_n_gram_lexicon, g_n_gram_lexicon, alpha, n_gram)
    gen_recall=get_recall(a_n_gram_lexicon, g_n_gram_lexicon,alpha,n_gram)
    f_beta=get_f_beta(beta,gen_precision,gen_recall)


    if len(g_punc)!=0 and len(a_punc)!=0:
        # for punctuation category
        p_gen_precision = get_precision_pun(a_punc, g_punc,lambda_p,n_gram)
        p_gen_recall = get_recall_pun(a_punc, g_punc, lambda_p,n_gram)
        p_f_beta = get_f_beta(beta, p_gen_precision, p_gen_recall)
        average_precision = (p_gen_precision + gen_precision) / 2
        average_recall = (p_gen_recall + gen_recall) / 2
        average_f_beta = get_f_beta(beta, average_precision, average_recall)
    else:
        average_f_beta=f_beta

    return average_f_beta



def get_ELEM(a_punc,g_punc,a_lexicon,g_lexicon,n_gram):
    alpha=3
    beta=1
    # beta=0.5
    lambda_p=0.1

    g_n_gram_lexicon = get_n_gram_lists(n_gram, g_lexicon)
    g_n_gram_punc = get_n_gram_lists(n_gram, g_punc)

    a_n_gram_lexicon = get_n_gram_lists(n_gram, a_lexicon)
    a_n_gram_punc = get_n_gram_lists(n_gram, a_punc)
    # a_lexicon, a_punc, a_number, a_operators=get_lex_punc_num_op_list(a_statement_list)
    # g_lexicon, g_punc, g_number, g_operators=get_lex_punc_num_op_list(g_statement_list)
    sum_TP_weights_l, sum_FP_weights_l, sum_FN_weights_l,_= get_sum_weights(a_n_gram_lexicon, g_n_gram_lexicon, alpha,
                                                                           n_gram)
    sum_TP_weights_p, sum_FP_weights_p, sum_FN_weights_p,_ = get_sum_weights_pun(a_n_gram_lexicon, g_n_gram_lexicon, alpha,
                                                                           n_gram)

    preceions = (sum_TP_weights_p + sum_TP_weights_l) / (sum_TP_weights_p + sum_TP_weights_l++1e-10) + (sum_FP_weights_p + sum_FP_weights_l++1e-10)
    recall = (sum_TP_weights_p + sum_TP_weights_l) / (sum_TP_weights_p + sum_TP_weights_l++1e-10) + (sum_FN_weights_p + sum_FN_weights_l++1e-10)



    # for lexical category
    # gen_precision=get_precision(a_lexicon, g_lexicon,alpha,n_gram)
    # gen_recall=get_recall(a_lexicon, g_lexicon,alpha,n_gram)
    gen_precision = get_precision(a_n_gram_lexicon, g_n_gram_lexicon, alpha, n_gram)
    gen_recall=get_recall(a_n_gram_lexicon, g_n_gram_lexicon,alpha,n_gram)
    f_beta=get_f_beta(beta,gen_precision,gen_recall)


    if len(g_punc)!=0 and len(a_punc)!=0:
        # for punctuation category
        p_gen_precision = get_precision_pun(a_punc, g_punc,lambda_p,n_gram)
        p_gen_recall = get_recall_pun(a_punc, g_punc, lambda_p,n_gram)
        p_f_beta = get_f_beta(beta, p_gen_precision, p_gen_recall)
        average_precision = (p_gen_precision + gen_precision) / 2
        average_recall = (p_gen_recall + gen_recall) / 2
        average_f_beta = get_f_beta(beta, average_precision, average_recall)

    else:
        f_b = 2 * preceions * recall / (preceions + recall)
        average_f_beta=f_beta

    return average_f_beta



def get_ELEM_accuracy(a_punc,g_punc,a_lexicon,g_lexicon,n_gram):
    alpha = 3
    lambda_p = 0.1
    g_n_gram_lexicon = get_n_gram_lists(n_gram, g_lexicon)
    g_n_gram_punc = get_n_gram_lists(n_gram, g_punc)

    a_n_gram_lexicon = get_n_gram_lists(n_gram, a_lexicon)
    a_n_gram_punc = get_n_gram_lists(n_gram, a_punc)

    gen_precision = get_precision(a_n_gram_lexicon, g_n_gram_lexicon, alpha, n_gram)

    sum_TP_weights_l, sum_FP_weights_l, sum_FN_weights_l,TN_l=get_sum_weights(a_n_gram_lexicon, g_n_gram_lexicon, alpha, n_gram)
    sum_TP_weights_p, sum_FP_weights_p, sum_FN_weights_p,TN_p = get_sum_weights_pun(a_punc, g_punc,lambda_p,n_gram)


    if len(g_punc) != 0 and len(a_punc) != 0:
        average_accuracy_p=sum_FP_weights_p+TN_p/len(g_punc)
        average_accuracy_l=sum_FP_weights_l+TN_l/len(g_lexicon)
        accuracy=(average_accuracy_p+average_accuracy_l)/2
    else:
        accuracy=0
    return accuracy



def calcualte(answer,generated,n_gram):
    g_statement_list, g_lexicon, g_punc, g_number, g_operators = to_ordered_list(generated_code)
    a_statement_list, a_lexicon, a_punc, a_number, a_operators = to_ordered_list(secure_ref_code)

    ELEM= get_ELEM(a_punc,g_punc,a_lexicon,g_lexicon,n_gram)
    ELEM_acc = get_ELEM_accuracy(a_punc, g_punc, a_lexicon, g_lexicon, n_gram)
    return ELEM


if __name__ == "__main__":
    calcualte()