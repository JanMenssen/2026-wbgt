%
% wbgt
%
%     class to retrieves WBGT data from the KNMI open data platfon
%
% modifications
%   16-jul-2026   JM    initial version

classdef wbgt < handle

  properties (Constant)
    TIMEZONE = 'Europe/Amsterdam';
    APIKEY = 'eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6IjBhZTg4MTI5MTAzOTQyN2FiMDVhNjM2NmNiOWQxMTE3IiwiaCI6Im11cm11cjEyOCJ9';
  end

  properties (Access = private)

    locationCode = [];
    locationName = [];

    startTime = [];
    endTime = [];
    
    api = [];
    wbgtData = [];

  end

  methods (Access = public)
    
    % constructor
    %
    %   set the default location and time

    function obj = wbgt(location)

      if nargin < 1, location = []; end
      if isempty(location), location = 'Gilze-Rijen'; end

      obj.setLocation(location);
      
      obj.startTime = datetime("now",'TimeZone',obj.TIMEZONE) - hours(6);
      obj.endTime = datetime("now",'TimeZone',obj.TIMEZONE);

      obj.api = OpenAPIData('wet_bulb_globe_temperature','3.0',obj.APIKEY);

    end

    % input
    %
    %     ask for the start and end - time

    function obj = input(obj)
  
      inputStr = sprintf('begin of WBGT data (%s) > ', string(obj.startTime, 'dd-MMM-yyyy HH:mm'));
      answer = input(inputStr','s');
      if ~isempty(answer),  obj.startTime = datetime(answer, 'InputFormat', 'dd-MMM-yyyy HH:mm',TimeZone=obj.TIMEZONE); end

      inputStr = sprintf('end of WBGT data   (%s) > ', string(obj.endTime, 'dd-MMM-yyyy HH:mm')');
      answer = input(inputStr,'s');
      if ~isempty(answer),  obj.endTime = datetime(answer, 'InputFormat', 'dd-MMM-yyyy HH:mm',TimeZone=obj.TIMEZONE); end

    end

    % setLocation
    %
    %     sets the location where the WBGT values should be obtained

    function obj = setLocation(obj,location)

      if strcmpi(location,"Gilze-Rijen")
        obj.locationCode = 6350;
        obj.locationName = "Gilze-Rijen";
      end

    end

    % readData
    %
    %     first find the files that are needed and next read the
    %     information into a table

    function obj = readData(obj)

      files = obj.api.list_files(obj.startTime,obj.endTime);
      nrItems = size(files,1);
      fprintf("%d files received ...\n",nrItems);

      obj.wbgtData = table('Size',[nrItems 3],'VariableTypes', {'datetime','double','double'},'VariableNames', {'time','wbgt','heatIndex'});
      obj.wbgtData.time.TimeZone = obj.TIMEZONE;

      modFactor = 1;
      if nrItems > 10, modFactor = 10; end
      if nrItems > 100, modFactor = 50; end
      
      % and for every file 

      for i=1:nrItems

        [obj.wbgtData.time(i),obj.wbgtData.wbgt(i),obj.wbgtData.heatIndex(i)] = obj.api.getWBGTdata(files(i).filename,obj.locationCode); 
        if (mod(i,modFactor) == 0), fprintf(1,"%d (of %d) files processed ...\n",i,nrItems); end
        if (i==nrItems), fprintf(1,"%d (of %d) files processed ...\n",i,nrItems); end

      end

      obj.wbgtData = obj.wbgtData(~isnat(obj.wbgtData.time),:);
      obj.wbgtData = sortrows(obj.wbgtData,'time');

    end

    % plot
    %
    %   makes a graph from the obtained wbgtData. With plotAerea, shaded
    %   areas can be set

    function obj = plot(obj,plotArea)
     
      if (nargin < 1), plotArea = []; end
      if isempty(plotArea), plotArea = true; end

      figure
      theme(gcf,"light")

      if (size(obj.wbgtData,1) < 50)
        hold on
        plot(obj.wbgtData.time,obj.wbgtData.wbgt,'*','MarkerSize',8,'Color',[0 0 1]);
        plot(obj.wbgtData.time,obj.wbgtData.wbgt,'LineWidth',1,'Color',[0 0 1]);
        hold off
      else
        plot(obj.wbgtData.time,obj.wbgtData.wbgt,'LineWidth',1.5,'Color',[0 0 1]);  
      end

      set(gca,'Box','on','YLim',[16 34])

      xlabel('Time',FontWeight='Bold');
      ylabel('WBGT (^oC)',FontWeight='Bold');
      title(sprintf("WBGT at %s",obj.locationName),FontWeight='Bold')

      % plot the shaded areas, See slide Hein Daanen

      if plotArea

        hold on

        yregion(32.15,34,'FaceColor',[1 0 0],'FaceAlpha',0.7);
        yregion(30.05,32.15,'FaceColor',[1 0 0],'FaceAlpha',0.5);
        yregion(27.85,30.05,'FaceColor',[1 0 0],'FaceAlpha',0.3);
        yregion(25.65,27.85,'FaceColor',[0.95 0.6 0],'FaceAlpha',0.45);
        yregion(22.25,25.65,'FaceColor',[0.9 0.9 0],'FaceAlpha',0.25);
        yregion(18.4,22.25,'FaceColor',[0.9 0.9 0],'FaceAlpha',0.15);

        yline(32.15,'k-','LineWidth',0.5);
        yline(30.05,'k-','LineWidth',0.5);
        yline(27.85,'k-','LineWidth',0.5);
        yline(25.65,'k-','LineWidth',0.5);
        yline(22.25,'k-','LineWidth',0.5);
        yline(18.4,'k-','LineWidth',0.5);

        hold off
      end
    end

    % list
    %
    %   makes a list of the WBGT data

    function obj = list(obj)

      disp(obj.wbgtData);
    
    end

  end
end
