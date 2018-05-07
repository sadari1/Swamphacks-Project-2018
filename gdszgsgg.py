def longestSubstringFinder(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        for j in range(len2):
            lcs_temp=0
            match=''
            while ((i+lcs_temp < len1) and (j+lcs_temp<len2) and string1[i+lcs_temp] == string2[j+lcs_temp]):
                match += string2[j+lcs_temp]
                lcs_temp+=1
            if (len(match) > len(answer)):
                answer = match
    return answer

print(longestSubstringFinder("dd apple pie available", "apple pies"))
print(longestSubstringFinder("cov_basic_as_cov_x_gt_y_rna_genes_w1000000", "cov_rna15pcs_as_cov_x_gt_y_rna_genes_w1000000"))
print(longestSubstringFinder("bapples", "cappleses"))
print(longestSubstringFinder("apples", "apples"))