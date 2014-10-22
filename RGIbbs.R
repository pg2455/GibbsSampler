num_mix<-2 # Number of mixtures
num_data<-10 # Number of data points
dim <-2 # Number of dimensions
sig <- 1
sigma <- sig*diag(dim) # Covariance matrix for x value
lam <- 1
lambda <- lam*diag(dim) # Covariance of mu values
iterations <- 20000 # Iterations of Gibbs

# Probabilities of categorical variable
Categorical <- runif(num_mix)
Categorical <- Categorical/sum(Categorical)

# Function to select category
category <- function(Categorical,num_mix){
  random_value <-runif(1)
  sum_probabilities <- 0
  for (i in 1:num_mix){
    sum_probabilities <- sum_probabilities + Categorical[i]
    if (sum_probabilities>random_value){
      return(i)
    }
  }
  return(num_mix)
}

# Means of normal 
normal_means <- vector(mode="list", num_mix)
for (i in 1:num_mix){
  normal_means[[i]] <- runif(dim)
}

# Generate data
x <- vector(mode="list", num_data)
cat <- 1:num_data
for (i in 1:num_data){
  cat[i]<-category(Categorical,num_mix)
  x[[i]]<-MASS::mvrnorm(1, normal_means[[cat[i]]], sigma)
}

# Update individual z_i
z_update_i <- function(mu,x_i,num_mix,dim,sig,Categorical){
  cat_i <- Categorical
  for (j in 1:num_mix){
    for (k in 1:dim){
      cat_i[j] <- cat_i[j]*dnorm( x_i[k],mu[[j]][k],sig )
    }
  }
  z_i<-category(cat_i/sum(cat_i),num_mix)
  return(z_i)
}

# Update z
z_update <- function(mu,x,num_mix,dim,sig,Categorical){
  z <- 1:num_mix
  for (i in 1:num_data){
    z[i]<-z_update_i(mu,x[[i]],num_mix,dim,sig,Categorical)
  }
  return(z)
}

# mu update
mu_update <- function(z,x,num_mix,num_data,dim,sig,lam){
  mu <- vector(mode="list", num_mix)
  for (i in 1:num_mix){
    n<-0
    x_bar<-c(0,0)
    for (j in 1:num_data){
      if (z[j]==i){
        n<-n+1
        x_bar<-x_bar+x[[j]]
      }
    }
    if(n>0){
      x_bar<-x_bar/n
      mu_i = (n/sig^2)/(n/sig^2+1/lam^2)*x_bar
      lam_i = 1/(n/sig^2+1/lam^2)
      mu[[i]]<-lam_i*rnorm(dim)+mu_i
    }
    else{
      mu[[i]]<-lam*rnorm(dim)
    }
  }
  return(mu)
}


# Create mu
mu <- vector(mode="list", num_mix)
for (i in 1:num_mix){
  mu[[i]] <- rnorm(dim)
}

# Create z
z <- ceiling(runif(num_data)*num_mix)

for (i in 1:iterations){
  mu<-mu_update(z,x,num_mix,num_data,dim,sig,lam)
  z<-z_update(mu,x,num_mix,dim,sig,Categorical)
}

print("Exact mu:")
print(normal_means)
print("Approximated mu:")
print(mu)
print("Exact z:")
print(cat)
print("Approximated z:")
print(z)