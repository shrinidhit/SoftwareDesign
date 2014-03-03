# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: YOUR NAME HERE
"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons
import random

def collapse(L):
    """ Converts a list of strings to a string by concatenating all elements of the list """
    output = ""
    for s in L:
        output = output + s
    return output

def codon_conversion(dnatriplet):
    """ Converts three letter DNA sequence to it's amino acid
    """
    for i in range(len(codons)): #checks if dna triplet is in every amino acid codon list
        if dnatriplet in codons[i]: #If dna triplet is in list, returns amino acid and exits sequence
            return aa[i]
    else:
        return "invalid codon" #if DNA sequence is invalid
        

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment
    """
    AAsequence = '' #initiates blank amino acid string
    for i in range(len(dna)/3): #repeats checking for codons at every full multple of 3
        AAsequence = AAsequence + codon_conversion(dna[(i*3):(i*3)+3]) #adds each amino acid to string
    return AAsequence #returns amino acid string

def coding_strand_to_AA_unit_tests():
    """ Unit tests for the coding_strand_to_AA function """
        
    #input with dna sequence of 9
    inp = 'ACGCGTTAG'
    output = coding_strand_to_AA(inp)
    print "input:" + inp + " expectedoutput: TR|" + " output:" + output;
    #input with dna sequence of 7
    inp = 'TTAGGATC'
    output = coding_strand_to_AA(inp)
    print "input:" + inp + " expectedoutput: LG" + " output:" + output;
    #input with dna sequence of 2
    inp = 'AC'
    output = coding_strand_to_AA(inp)
    print "input:" + inp + " expectedoutput:'' " + " output:" + output;
    

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    """
    compdna = '' #initializes complimentary DNA string
    #Returns opposite complimentary values
    for i in range(len(dna)-1,-1,-1):
        if dna[i] == 'T':
            compdna = compdna + 'A'
        elif dna[i] == 'C':
            compdna = compdna + 'G'
        elif dna[i] == 'A':
            compdna = compdna + 'T'
        elif dna[i] == 'G':
            compdna = compdna + 'C'
        else:
            return 'invalid base'
    return compdna #returns reverse string
    
def get_reverse_complement_unit_tests():
    """ Unit tests for the get_complement function """
        
    #input with all base types dna sequence of 9
    inp = 'ACGCGTTAG'
    output = get_reverse_complement(inp)
    print "input:" + inp + " expectedoutput: TGCGCAATC" + " output:" + output;
    #input with all base types and dna sequence of 7
    inp = 'TTAGGATC'
    output = get_reverse_complement(inp)
    print "input:" + inp + " expectedoutput: AATCCTAG" + " output:" + output;
    #input with invalid base
    inp = 'AH'
    output = get_reverse_complement(inp)
    print "input:" + inp + " expectedoutput: 'invalid base'" + " output:" + output;
    #input with no bases
    inp = ''
    output = get_reverse_complement(inp)
    print "input:" + inp + " expectedoutput: ''" + " output:" + output;

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    """
    # YOUR IMPLEMENTATION HERE
    endcut = len(dna) #first assumes entire sequence is one reading frame
    aasequence = coding_strand_to_AA(dna) #finds amino acid sequence
    for i in range(len(aasequence)): 
        if aasequence[i] == 'i': # checks if first letter of "invalid base" is present in aa sequence
            return 'invalid dna string'
        elif aasequence[i] == '|': #Checks for stop codon
            endcut = i*3;
            break
    return dna[0:endcut]
    

def rest_of_ORF_unit_tests():
    """ Unit tests for the rest_of_ORF function """
        
    #input with no stop codon
    inp = 'ACGCGTTCC'
    output = rest_of_ORF(inp)
    print "input:" + inp + " expectedoutput: ACGCGTTCC" + " output:" + output;
    #input with stop codon at end
    inp = 'CGATAG'
    output = rest_of_ORF(inp)
    print "input:" + inp + " expectedoutput: CGA" + " output:" + output;
    #input stop codon at beginning
    inp = 'TGA'
    output = rest_of_ORF(inp)
    print "input:" + inp + " expectedoutput: ''" + " output:" + output;
    #input with invalid base
    inp = 'CGAHCC'
    output = rest_of_ORF(inp)
    print "input:" + inp + " expectedoutput: 'invalid dna string'" + " output:" + output;
        
def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    #Prepares to calculate reading frames
    aa = coding_strand_to_AA(dna) #Gets amino acid sequence
    R_frames = [] #Intitializes reading frame matrix
    index = 0 #initializes index
    for i in range(index/3, len(aa)): #checks for start codon and adds index to Start matrix
        if aa[i] == 'M':
            newdna = dna[i*3:]
            R_frames.append(rest_of_ORF(newdna))
            index = index + len(R_frames[-1])/3 + 3
    return R_frames #returns reading frame matrix
    
def find_all_ORFs_oneframe_unit_tests():
    """ Unit tests for the find_all_ORFs_oneframe function """
   
    #input with no stop codon
    inp = 'ATGCGTTCC'
    output = find_all_ORFs_oneframe(inp)
    print "input:" + inp + " expectedoutput: ATGCGTTCC" + " output:" + str(output);
    #input with stop codon not in reading frame
    inp = 'ATGCGTGACC'
    output = find_all_ORFs_oneframe(inp)
    print "input:" + inp + " expectedoutput: ATGCGTGACC" + " output:" + str(output);
    #input with three stop codons
    inp = 'CGATAGATGTTTTAGGCATAG'
    output = find_all_ORFs_oneframe(inp)
    print "input:" + inp + " expectedoutput: [ATGTTT]" + " output:" + str(output);
    #input with invalid base
    inp = 'CGAHCC'
    output = find_all_ORFs_oneframe(inp)
    print "input:" + inp + " expectedoutput: 'invalid dna string'" + " output:" + str(output);
        
def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    #Getting ORF1 and initializing ORF2 and ORF3
    Orfs1 = find_all_ORFs_oneframe(dna) #Orfs for reading frame 1
    Orfs2 = find_all_ORFs_oneframe(dna[1:]) #Reading frame 2
    Orfs3 = find_all_ORFs_oneframe(dna[2:]) #Reading frame 3
    Orfs = Orfs1 + Orfs2 + Orfs3 #concatinating reading frames
    #removing exceptions
    while '' in Orfs:
        Orfs.remove('')
    while 'invalid dna string' in Orfs:
        Orfs.remove('invalid dna string')
    return Orfs

def find_all_ORFs_unit_tests():
    """ Unit tests for the find_all_ORFs function """
        
    #input with no stop codon in one reading frame, but one in the other
    inp = 'ATGCATGAATGTAG'
    output = find_all_ORFs(inp)
    print "input:" + inp + " expectedoutput: ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']" + " output:" + str(output);
    #simple input stop codon at beginning
    inp = 'TGA'
    output = find_all_ORFs(inp)
    print "input:" + inp + " expectedoutput: []'" + " output:" + str(output);
    #input with invalid base
    inp = 'CGAHCC'
    output = find_all_ORFs(inp)
    print "input:" + inp + " expectedoutput: []" + " output:" + str(output);
    
def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    """
    #Getting reverse dna
    reverse_dna = get_reverse_complement(dna) #Gets complimentary dna
    #Finding ORFs
    Orf_original = find_all_ORFs(dna)
    Orf_reverse = find_all_ORFs(reverse_dna)
    #Total ORFs
    Orf = Orf_original + Orf_reverse #concatinates and returns orfs
    return Orf
    

def find_all_ORFs_both_strands_unit_tests():
    """ Unit tests for the find_all_ORFs_both_strands function """
    #complex input
    inp = 'ATGCGAATGTAGCATCAAA'
    output = find_all_ORFs_both_strands(inp)
    print "input:" + inp + " expectedoutput: ['ATGCGAATG', 'ATGCTACATTCGCAT']" + " output:" + str(output);
    #simple input stop codon at beginning
    inp = 'TGA'
    output = find_all_ORFs_both_strands(inp)
    print "input:" + inp + " expectedoutput: []'" + " output:" + str(output);
    #input with invalid base
    inp = 'CGAHCC'
    output = find_all_ORFs_both_strands(inp)
    print "input:" + inp + " expectedoutput: []" + " output:" + str(output);

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string"""
    #gets all Orfs
    all_Orfs = find_all_ORFs_both_strands(dna)
    #if Orfs is empty, returns empty matrix
    if all_Orfs == []:
        return ''
    #if Orfs is not empty, returns longest ORf
    else:
        longest_ORF = max(all_Orfs, key=len)
        return longest_ORF

def longest_ORF_unit_tests():
    """ Unit tests for the longest_ORF function """
    
    inp = 'ATGCGAATGTAGCATCAAA'
    output = longest_ORF(inp)
    print "input:" + inp + " expectedoutput: 'ATGCTACATTCGCAT'" + " output:" + str(output);

def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    dna_list = list(dna) #converts dna string to list
    out= [] #intitializes output
    #shuffles dna for number of trials, and returns maximum length
    for i in range(num_trials):
        random.shuffle(dna_list) #shuffles list
        new_dna = collapse(dna_list) #turns list into string
        out.append(len(longest_ORF(new_dna))) #adds longest gene length to out
        final_ORF = max(out) #returns maximum of out
        return final_ORF

def gene_finder(dna, threshold):
    """ Returns the amino acid sequences coded by all genes that have an ORF
        larger than the specified threshold.
        
        dna: a DNA sequence
        threshold: the minimum length of the ORF for it to be considered a valid
                   gene.
        returns: a list of all amino acid sequences whose ORFs meet the minimum
                 length specified.
    """
    total_list = find_all_ORFs_both_strands(dna)
    final_list = [] #intializes final list
    #checks if total list's reading frame lengths are greater than threshold, and adds to final list if it does
    for i in range(len(total_list)):
        if len(total_list[i]) >= threshold:
            final_list.append(total_list[i])
    return final_list #returns new filtered list
