A suspended research project that modify stock market data and reproduces the results of other scholars's essay. But it remains to provide useful research framworks for price prediction if in finance area.

1. data_obtain.ipynb:
Obtain stock market data via API from CSMAR Database

2. factor_construct.ipynb:
Construct factors using raw data, classified by genre mentioned in the refered paper, and write code by own understanding according to instructions in paper appendix. Also define some auxiliary python functions to help extract single variable from raw data and calculate features adjusted by industries.

3. run_model.ipynb:
Regularize time frequency, impute missing values, combine features, drop missing records, add dummy variables of industry and finally define portfolio strategy and backtest its performance using models like LinearRegression, Ridge, Lasso, ElasticNet, SVR and XGBoost Tree

reference:
1. M. Leippold, Q. Wang and W. Zhou, Machine learning in the Chinese stock market, Journal of Financial Economics, https://doi.org/10.1016/j.jfineco.2021.08.017
2. 李斌, 邵新月, 李玥阳, 机器学习驱动的基本面量化投资研究, 《中国工业经济》, 10.19581/j.cnki.ciejournal.2019.08.004