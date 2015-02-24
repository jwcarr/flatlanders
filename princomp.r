raw_scores<-read.table('pca_input.csv', sep=',')
x<-prcomp(raw_scores, scale=TRUE)
choices = 1:NCOL(x$x)
scale = 1
pc.biplot = FALSE
scores<-x$x
lam <- x$sdev[choices]
n <- NROW(scores)
lam <- lam * sqrt(n)
lam <- lam^scale
xx<-t(t(scores[, choices])/lam)
write.table(xx, file='pca_output.csv', sep=',')
pc_sum<-summary(x)
prop_var<-pc_sum$importance[2,]
write.table(prop_var, file='pca_output_pv.csv', sep=',')