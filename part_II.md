# Technical evaluation part 2 #
You have 30 mins to complete this part of technical evaluation. Provide the answers as a text file and email to marcela.davila@gu.se at the end of the allocated session. Good luck!

**1.In case the time given for the practical task was not enough for you to finish, explain as detailed as possible, what is left to do and why was not possible to complete a working version of this script.**

*Ans:* I have written the Python script that can both run once or as a `watchdog` process. It sends out an email to specified user in case of a failed run.
Things that might improve it:

A. Containerize the script (Singularity/ Docker)
B. Instead of using Python `watchdog` use some other system level task schedular such as CRON jobs so that we don't need the script running all the time.
C. Also add a database of processed samples for recordkeeping and to avoid re-running the script on already processed data.

**2.A research group sequenced 900 patients with highly heterogeneous cancer like Hepatocellular Carinoma. Patients' have matched adjacent normals samples.**

**a. Describe a workflow to perform a DE gene analysis as well as gene set enrichment analysis. Justify any programs, databases and statistical tests you would use.**

*Ans:* The workflow should be:
A. Data pre-processing

Quality control: `MultiQC`/ `FASTQC`/ `FASTP`: Remove low quality bases, contamination and verify the integrity of the samples

Trimming: `Trimmomatic`/ `Cutadapt`: Remove adapters and low quality overhangs

Alignment: `STAR`/ `HISTA2`: Align reads to the human reference genome

Quantification: If using `STAR` simply enable quantification, or use programs such as `Salmon`/`Kallisto`. This would give us raw gene counts.

B. Normalization and differential gene expression analysis

These two steps are performed using the same program, `DESeq2` or it's Python counterpart, `pyDESeq2`. The program uses negative binomial distribution for modelling the count data. The results are in log2 fold change values and p-values are corrected. We can select genes with false discovery rate of < 0.05 as significant ones. The log2 fold change cut off varies based on the biological question.

C. Gene set enrichment analysis (GSEA)

R package `clusterProfiler` is widely used for this purpose and can perform this part. Please note that GSEA uses the complete differential expression matrix rather than only the significant genes part. There are various human cancer specific databases that can be used to solve this biological query.

D. Visualizations:
R `GGPlot2`, `clusterProfiler` and `pheatmap` can be used to plot heatmaps, volcano plots and GSEA plots.

**b. Discuss any limitations we should be aware to perform this kind of analysis**

*Ans:* There are potential limitations and pitfalls that one must be aware of while performing this kind of study. One of the major biological problems are with the tumor heterogeneity which can potentially obscure the results. This can be solved by more robust statistical models to account for subclonal populations.

One must keep a close and vigilant eye on the batch effetc, low sample size, confounding variables and sample processing delays as common technical caveats.


**c. These heatmaps show the gene expression of the samples (A) and their DE analyses (FDR<0.05), what are your comments to the researcher?**

*Ans:* There is a strong separation of expression profiles between tumor and normal samples, which is expected and hence increases confidence in the analysis. As from the figure B, one can say that there is an evident separation of samples expression profile but it doesn't seem to strongly match with any of the phenotypes. There might be a confounding variable that needs normalization or put into the model. Also important to note here are the samples in around the middle which show `no-change` for most of the genes. These must be investigated as they are the unique cluster.

**3.You are working with 3 consulting projects. One is a differential expression analysis from microarray data. The second is the analysis of TMT data that you got from the Proteomics facility while the third is the identification of a virus integration in some clinical samples. You will be delivering the results sometime during next week, as agreed with the different users. A fourth user got the reviewer’s comments and they need to answer back in a week, so they need your help during this week. What would you do?**

*Ans:* Given the fact that I come from the same field, I understand the urgency of such review processes, I would accomodate this new person in the workflow even if it means working a bit extra on a few days.

**4.During a first meeting consultation, the analysis that the group is asking you to do is quite new and you haven’t performed it before. As usual, they need results in as soon as possible for a grant application. What would you do?**

*Ans:* I would clearly let them know the situation and to minimize the risk, ask them to seek another expert from the team who is well versed with the method or in case they wish to still carry forward with me, I would proceed with their approval. I don't wish someone to fail their grant application because I promised more than I could.


**5.After having delivered the final results to a user, you are contacted by the PI saying that the results you delivered do not make sense. You check them and you realize you made a mistake in one of the calculations. What would you do?**

*Ans:* Admit my mistake, thank the PI for being deligent and deliver the updated results with the highest priority.