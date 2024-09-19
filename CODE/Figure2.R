## Packages ##
library(dplyr)

## Read SWE insitu information ##
SWE_IF <- read.table("SWE_Insitu_data_info.txt", sep=";", header=T)

## Calculate statistic of insitu dataset ##
SWE_IF$Day_Count_yr <- SWE_IF$Day_Count / 365
SWE_IF$Day_Count_yr <- SWE_IF$Day_Count_yr %>% as.numeric()

h_elv <- hist(SWE_IF$ELV, freq=T, breaks=seq(0,6200,100))
elv_f <- c(h_elv$counts[1],
           h_elv$counts[2:5] %>% sum(),
           h_elv$counts[6:10] %>% sum(),
           h_elv$counts[11:20] %>% sum(),
           h_elv$counts[21:62] %>% sum()) 

h_dct <- hist(SWE_IF$Day_Count_yr, breaks = seq(0,60,10), freq=F)

yrc_f <- c(h_dct$counts[1],
           h_dct$counts[2],
           h_dct$counts[3],
           h_dct$counts[4],
           h_dct$counts[5])


## Draw the histogram 
elv_fg <- barplot(elv_f, 
           ylim = c(0,5000),
           cex.axis = 2.5,
           cex.lab = 2
           )
axis(1,at=elv_fg, labels = c("<100", "100-500", "500-1000", "1000-2000", ">2000"), cex.axis = 2.5, mgp = c(3, 1.8, 0) )
title(ylab = "N", line = 4, cex.lab = 2.8)
title(xlab = "meas. elev", line = 4.2, cex.lab = 2.8)

yrc_fg <- barplot(yrc_f, 
                  ylim = c(0,10000),
                  cex.axis = 2.3,
                  cex.lab = 2)
axis(1,at=yrc_fg, labels =  
       c("<5", "5-10",
         "10-15","15-20",
         ">20"), cex.axis = 2.5, mgp = c(3, 1.8, 0))
title(xlab = "data length", line = 4, cex.lab = 2.5) 
title(ylab = "N", line = 4, cex.lab = 2.8)

