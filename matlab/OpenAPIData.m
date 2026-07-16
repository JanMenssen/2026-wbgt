% 
% OpenAPIdata
%
%     this class handles the KNMI Open Data API. Currenlty the following
%     methods are implemented
%
%         - list_files : returns a list of files between start and stoptime
%         - getWBGTdata : returns the WBGT value for a given wheaterStation
%
% modifications
%     16-jul-2026   JM    initial version

classdef OpenAPIData < handle

  properties (Access = private)

    baseUrl = [];
    apikey = [];

  end

  methods (Access = public)
  
    % constructor
    %
    %   sets the used dataset and version. If the user has a private
    %   token it can also be set

    function obj = OpenAPIData(dataset,version,token)
  
      obj.apikey = token;
      obj.baseUrl = ['https://api.dataplatform.knmi.nl/open-data/v1/datasets/' dataset '/versions/' version];

    end
    
    % list_files
    %
    %   returns a list of files between the start time and end time

    function files = list_files(obj,startTime,endTime)

      files = [];

      % convert to KNMI (string) format

      starttime = startTime - hours(2);
      endtime = endTime - hours(2); 

      knmiStart = sprintf('wbgt_%s.csv',string(starttime,'yyyyMMddHHmm'));
      knmiEnd = sprintf('wbgt_%s.csv',string(endtime,'yyyyMMddHHmm'));
      
      % create the base url 

      options = weboptions('HeaderFields', {'Authorization', obj.apikey},'ContentType','json','Timeout',30);

      % and get the first files

      url = sprintf('%s/files/?maxKeys=1000&sorting=desc&orderBy=filename&begin=%s&end=%s',obj.baseUrl,knmiStart,knmiEnd);

      data = webread(url,options);

      if isfield(data,'files'), files = [files ; data.files]; end

      % check all files are send, if not get the others

      while (isfield(data,'nextPageToken'))

        url = sprintf('%s?maxKeys=1000&sorting=desc&orderBy=filename&begin=%s&end=%s&nextPageToken=%s',obj.baseUrl,knmiStart,knmiEnd,data.nextPageToken);
        data = webread(url, options);

        files = [files; data.files];

        pause(0.5);  % tegen 429
      end

    end

    % getWBGTdata
    %
    %   given a filename and the weatherStation, this method returns the
    %   WBGT and heatIndex. The file is read adn searched on <weatherStation>

    function [timestamp,wbgt,heatIndx] = getWBGTdata(obj,filename,weatherStation)

      wbgt = NaN;
      heatIndx = NaN;
      timestamp = NaT;

      % check the date of the file is between starttime and endtime, if not the
      % routine can be leaved

      strTimeStamp = char(filename);
      timefile = datetime(strTimeStamp(6:17),'InputFormat','yyyyMMddHHmm',TimeZone='Europe/Amsterdam');
      timefile = timefile + hours(2);

      downloadUrl = sprintf("%s/files/%s/url",obj.baseUrl,filename);
      options = weboptions('HeaderFields', {'Authorization', obj.apikey},'ContentType','json','Timeout',30);

      % get a tempory link and download the file ;

      try

        fileInfo = webread(downloadUrl, options);
        outFile = websave(filename,fileInfo.temporaryDownloadUrl);

        % read the file 

        t = readtable(outFile);

        % and find for the selected weather station

        station_row = t(t.station == weatherStation,:);
        if ~isempty(station_row)
          wbgt = station_row.wbgt;
          heatIndx = station_row.heat_force;
          timestamp = timefile;
        end

        % delete the file

        delete(outFile);

      catch ME
        if contains(ME.message,'429'), fprintf('error 429 received for file %s...\n',filename); end
      end

    end
    
  end

end