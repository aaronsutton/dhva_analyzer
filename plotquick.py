import return_DataToPlot as DP

UnSortCurrentH,CurrentT,A1X,A1Y,A2X,A2Y,B1X,B1Y,B2X,B2Y,C1X,C1Y,C2X,C2Y,E,F = DP.return_DataToPlot('2012_02_09_02_NCCO_000.nc')
plot(UnSortCurrentH,C1X,'b.')
xlim(2.07,15)
xlabel('Field (T)')
ylabel('Signal (V)')
title('Nd$_{1.85}$Ce$_{0.15}$CuO$_4$ Susceptibility')
savefig('test.eps')