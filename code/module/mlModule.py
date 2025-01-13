import os
import pandas
from config import config
from prototype.module import Module
from moduleResult.mlResult import MLResult

class MLModule(Module):
    def __init__(self, strategy="topdown", thresh=0.45, gen='gen1'):
        self.strategy = strategy
        self.thresh = thresh
        self.gen = gen
        super().__init__(f'ML-stratgy={strategy};th={thresh}, gen={gen}')
        # self.baseName = self.moduleName
        self.resultDict = dict()
        if self.gen == 'gen1':
            self.esultFileNames = {
                "realm": f"{config.MLResultFolder}/gen1_realm_t33_512_5_result.csv.predictions_with_contig_level_scores_res_noUnknown.csv",
                "kingdom": f"{config.MLResultFolder}/gen1_kingdom_realm_finetune_t33_256_12_result.csv.predictions_with_contig_level_scores_res_noUnknown.csv",
                "phylum": f"{config.MLResultFolder}/gen1_phylum_realm_kingdom_finetune_t33_256_12_result.csv.predictions_with_contig_level_scores_res_noUnknown.csv",
                "class": f"{config.MLResultFolder}/gen1_class_t33_256_12_result.csv.predictions_with_contig_level_scores_res_noUnknown.csv",
                "order": f"{config.MLResultFolder}/gen1_order_t33_512_5_result.csv.predictions_with_contig_level_scores_res_noUnknown.csv",
                "family": f"{config.MLResultFolder}/gen1_family_order_finetune_t33_512_5_result.csv.predictions_with_contig_level_scores_res_noUnknown.csv",
                "genus": f"{config.MLResultFolder}/gen1_genus_order_family_finetune_t33_256_12_result.csv.predictions_with_contig_level_scores_res_noUnknown.csv",
            }
        elif self.gen == 'gen2':
            self.resultFileNames = {
                "realm": f"{config.MLResultFolder}/gen2_realm_t33_512_5_result.csv.predictions_with_contig_level_scores_res_noUnknown.csv",
                "kingdom": f"{config.MLResultFolder}/gen2_kingdom_t33_256_12_result.csv.predictions_with_contig_level_scores_res_noUnknown.csv",
                "phylum": f"{config.MLResultFolder}/gen2_phylum_t33_512_4_result.csv.predictions_with_contig_level_scores_res_noUnknown.csv",
                "class": f"{config.MLResultFolder}/gen2_new_class_t33_512_4_result.csv.predictions_with_contig_level_scores_res_noUnknown.csv",
                "order": f"{config.MLResultFolder}/gen2_order_t33_512_5_result.csv.predictions_with_contig_level_scores_res_noUnknown.csv",
                "family": f"{config.MLResultFolder}/gen2_family_order_finetune_t33_512_5_result.csv.predictions_with_contig_level_scores_res_noUnknown.csv",
                "genus": f"{config.MLResultFolder}/gen2_genus_enlarge_family_finetune_t33_256_10_result.csv.predictions_with_contig_level_scores_res_noUnknown.csv",
            }

        
    def run(self):

        files = list(self.resultFileNames.values())
        if (self.strategy.startswith('bottomup')):
            files = reversed(files)

        for file in files:
            df = pandas.read_csv(file)
            for row in df.itertuples():
                query = row.seq_name
                score = row.prediction_score
                res = row.taxa_prediction

                if (query not in self.resultDict):
                    self.resultDict[query] = MLResult(self.strategy, self.thresh)
                self.resultDict[query].addResult(res, score)

        # resultFile = f"{config.resultBase}/{self.baseName}.csv"
        # self.resultDict = dict()
        # if (os.path.exists(resultFile)):
        #     with open(resultFile) as fp:
        #         fp.readline()
        #         for line in fp:
        #             terms = line.strip().split(',')
        #             self.resultDict[terms[0]] = terms[1]
    
    def getResult(self, sample):        
        if (sample.id in self.resultDict):
            return self.resultDict[sample.id]
        else:
            return None