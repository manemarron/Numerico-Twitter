library(Matrix)
library(ggplot2)
library(ggfortify)
library(rgl)

term_freq <- read.csv("term_freq.csv",header = TRUE)
words <- data.frame(fread("words.csv"))
X <- sparseMatrix(i = term_freq$i, j = term_freq$j, x = term_freq$x)
dimnames(X)[[2]] <- as.vector(words$word)
z <- princomp(X, scale = TRUE, scores = TRUE)

## Gráfica 2d
ggplot2::autoplot(z, 
  label = FALSE,
  colour = "yellow",
  loadings.label = TRUE,
  loadings.colour = "blue",
  xlim = c(-0.5,1.0),
  ylim = c(-1,1))

## Gráfica 3d
text3d(z$loadings[,1:3], texts=rownames(z$loadings), col="red")
coords <- NULL
for (i in 1:nrow(z$loadings)) {
  coords <- rbind(coords, rbind(c(0,0,0),z$loadings[i,1:3]))
}
lines3d(coords, col="blue", lwd=4)