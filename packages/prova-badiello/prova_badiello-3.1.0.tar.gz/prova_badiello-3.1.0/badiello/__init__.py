def aiutino():
    stringa = '''
generan=function(n,x0,a,b,m){
  ris=rep(NA,n)
  ris[1]=x0 # Il primo valore generato e' il valore iniziale.
  for (i in 2:n){
    ris[i]=(a*ris[i-1]+b)%%m
  }
  return(list(int=ris,unif=ris/m))
}


p = generan(200, 40, 1, 8, 81)
plot(p$int, type = "l")
#acf(p$int) # I valori generati sono correlati!

p = generan(200, 1, 401, 101, 1024)
plot(p$int, type = "l")
#acf(p$int)

p = generan(200, 1, 1664525, 1013904223, 2^32)
plot(p$int, type = "l")
#acf(p$int)

p = generan(200, 2, 1664525, 1013904223, 2^32)
plot(p$int, type = "l") # Cambiando solo il valore iniziale,
# i valori generati cambiano
# completamente.
#acf(p$int)


.current.seed <- c(123, 456, 789)
runif.wh <- function(n){
  a <- c(171, 172, 170)
  b <- c(30269, 30307, 30323)
  s <- .current.seed
  u <- rep(0, n)
  for (i in 1:n){
    s <- (a * s)%%b
    u[i] <- sum(s/b)%%1
  }
  .current.seed <<- s
  u
}

.current.seed
runif.wh(3)

.current.seed
runif.wh(3)


# Importanza di usare <<- invece di <-

s <- 1
f1 = function() s <- 3
f2 = function() s <<- 5

f1()
s # s non cambia
f2()
s # s cambia


.current.seed <- c(123, 456, 789)
runif.wh(3)


args(runif) # ?args per informazioni su args

runif(3)

set.seed(1)
runif(3)
set.seed(1)
runif(3)

?Random # "... '.Random.seed' can be saved and restored,
#  but should not be altered by the user."
# "'.Random.seed' saves the seed set for the uniform random-number
# generator. It does not necessarily save the state of other generators.
# If you want to reproduce work later, call 'set.seed'."
RNGkind() # Il generatore di default e' quello di Mersenne-Twister,
# di Matsumoto e Nishimura (1998).



u <- runif.wh(1e+05)
plot(ecdf(u), do.points = FALSE) # Il valore di default di do.points e' TRUE solo
# per n < 1000. Quindi il comando che stiamo dando
# e' equivalente a plot(ecdf(u)).
curve(punif(x), col = "red", add = TRUE)

plot(sort(u), ((1:length(u)) - 0.5)/length(u))
abline(0, 1)


b <- seq(0,1,by=0.2)
b

q <- length(b)-1 # Numero di intervallini.
q

plot(b,b,type="n") # Prepariamo il grafico, senza disegnare nulla.
for ( i in 1:length(b) ) abline(h=b[i],lty=2)
for ( i in 1:length(b) ) abline(v=b[i],lty=2)

freq <- table(cut(u[-1], breaks = b), cut(u[-length(u)], breaks = b))
nm1 <- sum(freq) # Questo e' il numero di coppie di valori successivi (u_i, u_{i-1}),
# ossia n-1.
nm1
round(freq/nm1, 4) # Dovrebbero essere valori vicini a 1/q^2.

attese <- nm1/q^2
X2 <- sum((freq - attese)^2/attese)
c(X2, 1 - pchisq(X2, q^2 - 1))

# Per verificare, in generale, con il test X^2 la dipendenza per ritardo k,
# bisogna considerare tutte le coppie (u_i, u_{i-k}).


acf(u, ylim = c(-1, 1))

plot(u[-length(u)], u[-1], pch = ".")


u <- generan(1e5, 1, 1664525, 1013904223, 2^32)$unif
plot(ecdf(u), do.points = FALSE)
curve(punif(x), col = "red", add = TRUE)
plot(sort(u), ((1:length(u)) - 0.5)/length(u))
abline(0, 1)
freq <- table(cut(u[-1], breaks = b), cut(u[-length(u)], breaks = b))
nm1 <- sum(freq) # Questo e' il numero di coppie di valori successivi (u_i, u_{i-1}).
round(freq/nm1, 4)
attese <- nm1/q^2
X2 <- sum((freq - attese)^2/attese)
c(X2, 1 - pchisq(X2, q^2 - 1))
acf(u, ylim = c(-1, 1))
plot(u[-length(u)], u[-1], pch = ".")


x <- 1:10
x
a <- cut(x, breaks = c(0, 5, 10))
a
is.factor(a)

x[1]
x[-1]


runif.wh1 <- function(n) {
  a <- c(171, 172, 170)
  b <- c(30269, 30307, 30323)
  s <- .current.seed
  u <- NULL
  for (i in 1:n) {
    s <- (a * s)%%b
    u <- c(u, sum(s/b)%%1)
  }
  .current.seed <<- s
  u
}

.current.seed <- c(123, 456, 789)
runif.wh(3)

.current.seed <- c(123, 456, 789)
runif.wh1(3)

t1 = system.time(runif.wh(5000))
t2 = system.time(runif.wh1(5000))

t1 # Ci interessa solo il terzo valore, che e' il tempo
# "realmente" usato dalla procedura.
t2

a1 = t2[3]-t1[3] # Differenza nel tempo di calcolo senza e con preallocazione.

t1 = system.time(runif.wh(1e+05))
t2 = system.time(runif.wh1(1e+05))

a2 = t2[3]-t1[3] # Differenza nel tempo di calcolo senza e con preallocazione.

a2/a1

# Aumentando n di 20 volte, la differenza nei tempi
# di calcolo aumenta di molto piu' di 20 volte.

###############################################################################

dlaplace <- function(y, a = 0, b = 1) {
  exp(-abs(y - a)/b)/(2 * b)
}

curve(dlaplace(x, 0, 1), -10, 10, lty = "solid")
curve(dlaplace(x, 0, 4), -10, 10, lty = "dashed", add = TRUE)
curve(dlaplace(x, 4, 1), -10, 10, lty = "dotted", add = TRUE)

plaplace <- function(y, a = 0, b = 1) {
  (1 + sign(y - a) * (1 - exp(-abs(y - a)/b)))/2
}

qlaplace <- function(p, a = 0, b = 1) {
  a - b * sign(p - 0.5) * log(1 - 2 * abs(p - 0.5))
}

curve(plaplace(x,0,1),-10,10,lty=1)
curve(plaplace(x,0,4),lty=2,add=TRUE)
curve(plaplace(x,4,1),lty=2,add=TRUE)

curve(qlaplace(x,0,1),0,1,lty=1,ylim=c(-10,10))
curve(qlaplace(x,0,4),lty=2,add=TRUE)
curve(qlaplace(x,4,1),lty=2,add=TRUE)

rlaplace <- function(n, a = 0, b = 1) {
  qlaplace(runif.wh(n), a, b)
}

y <- rlaplace(1e+05)
plot(ecdf(y), do.points = FALSE, xlim = c(-6, 6))
curve(plaplace(x), -10, 10, add = TRUE, col = "red")

Box.test(y, 100, "L")


x=c(1,2,4,7)
pr=c(0.2,0.4,0.1,0.3)
xx=cut(runif(1000),breaks=c(0,cumsum(pr)),labels=c(1,2,4,7))
table(xx)

# Come funziona "while".

i = 0 # Inizializzazione.
while (i < 7){ # Condizione: se e' vera continuo.
  print(i)
  i = i + 1
}

# La funzione di ripartizione di una Poisson, nella sintassi di R,
# è definita come:

ppois.mia = function(x,lambda) {
  x = floor(x) # Arrotonda all'intero più piccolo
  # (serve quando x è frazionario)
  x=0:x
  exp(-lambda) * sum(lambda^x/factorial(x))
}

# Qui sotto usiamo la funzione ppois, predefinita in R.

F = function(x) ppois(x, 3) # Voglio generare da una Pois(3).
generaF = function() { # Genero un singolo valore.
  u = runif(1)
  valore = 0
  while (F(valore) < u) {
    valore = valore + 1
  }
  return(valore)
}


x = rep(NA, 10000)
system.time(for (i in 1:10000) x[i] = generaF())


# Come funziona "all".

x = 1:4
all(x < 1)
all(x < 3)
all(x < 5)
all(!(x<1))

# Come funziona "repeat".

x = 1:4
repeat {
  x = x + 1
  cond = x > 4
  if (all(cond)) break # Con "break" esco dal ciclo "repeat".
}

F = function(x) ppois(x, 3)
generaFn = function(n) { # Genero n valori.
  u = runif(n)
  valore = rep(0, n)
  repeat {
    ind = F(valore) < u
    valore[ind] = valore[ind] + 1
    if (all(!ind)) break
  }
  return(valore)
}

# Provare "a mano" i passi della funzione appena scritta,
# partendo ad esempio da u = c(0.1,0.5,0.15,0.7).

# Invece che con "repeat", generaFn poteva essere implementata usando
# "while", precisamente con

# while(any(ind)) {...}

# Si noti che any(v) restituisce TRUE se almeno uno degli elementi
# del vettore logico v è TRUE. Ad esempio

x = 1:4
any(x < 1)
any(x < 2)
any(x < 5)

# Implementazione di generaFn con while.

generaFn.w = function(n) { # Genero n valori.
  u = runif(n)
  valore = rep(0, n)
  ind = rep(T,n) # In questo caso devo inizializzare ind.
  while(any(ind)) { # Uso while invece di repeat.
    ind = F(valore) < u
    valore[ind] = valore[ind] + 1
  }
  return(valore)
}

###

x = rep(NA, 10000)
system.time(for (i in 1:10000) x[i] = generaF())
system.time(generaFn(10000))

###############################################################################

r.acc.rif <- function(n, f, g, rg, k, report = TRUE) {
  y <- double(n)
  ntry <- 0
  for (i in 1:n) {
    done <- FALSE
    while (!done) {
      ntry <- ntry + 1
      z <- rg(1)
      u <- k * g(z) * runif.wh(1)
      if (u <= f(z))
        done <- TRUE
    }
    y[i] <- z
  }
  if (report)
    cat("tentativi:", ntry)
  y
}

curve(dlaplace(x), -6, 6, col = "red", lwd = 2)
curve(dnorm(x), -6, 6, add = TRUE, lwd = 2)

k <- sqrt(2 * exp(1)/pi)
curve(k * dlaplace(x), -6, 6, lty = "dotted", lwd = 2)
curve(dlaplace(x), -6, 6, lty = "dashed", add = TRUE)
curve(dnorm(x), -6, 6, add = TRUE)

rnorm.ar <- function( n , mu=0 , sigma=1 , verbose = TRUE ) {
  k <- sqrt(2*exp(1)/pi)
  mu + sigma *
    r.acc.rif(n,
              dnorm,
              dlaplace,
              rlaplace,
              k,
              verbose)
}

y <- rnorm.ar(1e+05)

# Numero atteso di tentativi:

k * 1e+05

c(mean(y), sd(y)) # I valori generati hanno (approssimativamente)
# media 0 e deviazione standard 1


plot(ecdf(y),do.points=FALSE, xlim=c(-4,4))
curve(pnorm(x),-4,4,col="red",add=TRUE)
hist(y,prob=TRUE,nclass=100)
curve(dnorm(x),-5,5,add=TRUE)

acf(y, 100, ylim = c(-1, 1), demean = FALSE)

###############################################################################

f=function(x) dbeta(x,2,3)
x=y=rep(NA,100)
x[1]=0.5
y[1]=0.1
simsufy=function(y) {
  u=runif(1,0,1) # Genero uniformemente sul supporto [0,1] della beta.
  while (f(u)<y) u=runif(1,0,1) # Accetto il valore u generato solo se f(u) > y.
  u # Questo valore è generato uniformemente sulla "fetta" {x: f(x) > y}.
}
for (i in 2:10000){
  y[i]=runif(1,0,f(x[i-1]))
  x[i]=simsufy(y[i])
}

hist(x,prob=T,nclass=50)
curve(f(x),add=TRUE,col="red")

print("Finito")

'''
    print(stringa)
