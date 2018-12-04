library(readr)
library(itertools)
#dev.off()
rm(list=ls())
setwd(choose.dir(getwd(), "Choose working Directory"))

number_of_files = 12

iner_radius = 2.5
outter_radius = 62.5
density_mat = 1.4
thickness = 13


volume = 3.1416 * (outter_radius^2 - iner_radius^2) * thickness
mass = volume * density_mat

efficiency_calculater <- function(file, mass){
  spec_data <- read_table2(file, col_names = FALSE, skip = 6, comment = "#")
  plot(spec_data$X1,spec_data$X2, "l")
  interval_enr = spec_data$X1[1]*2
  efficiency = sum(spec_data$X2*interval_enr) * mass
  return(efficiency)
}

efficiency_df <- data.frame(matrix(vector(), number_of_files, 1, 
                                   dimnames = list(c(), c("Efficiency"))),
                            stringsAsFactors = F)

layer = 4 
for (i in 1:number_of_files) {
  file = sprintf("KP_Ra_%i_6.txt", layer)
  efficiency_df$Efficiency[i] <- efficiency_calculater(file = file, mass= mass)
  layer = layer + 7
}

write.csv(efficiency_df, "Efficiency_mass.csv")
