function getWBGT
%% getWBGT            retrieves WBGT info from KNMI weather data
%
%   retrieves the latest WBGT and heat force from the weather station
%   Gilze-Rijen (=6350)
%
% modifications
%    18-jun-2026 JM   initial version
%    23-jun-2026 JM   start and enddate are asked
%    23-jun-2026 JM   APIKEY in function
%    14-jul-2026 JM   small bug removed from graphics
%    16-jul-2026 JM   now makes use of external classes

  addpath('matlab')

  myWBGT = wbgt("Gilze-Rijen");
  
  myWBGT = myWBGT.input();
  myWBGT = myWBGT.readData();
  myWBGT = myWBGT.plot(true);
  myWBGT = myWBGT.list()






