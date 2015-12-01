library(Matrix)
library(ggplot2)
library(ggfortify)
term_freq <- read.csv("term_freq.csv",header = TRUE)
words <- data.frame(fread("words.csv"))
X <- sparseMatrix(i = term_freq$i, j = term_freq$j, x = term_freq$x)
dimnames(X)[[2]] <- as.vector(words$word)
ggplot2::autoplot(
  princomp(X, scale = TRUE), 
  label = FALSE,
  colour = "yellow",
  loadings.label = TRUE,
  loadings.colour = "blue",
  xlim = c(-0.5,1.0),
  ylim = c(-1,1))
