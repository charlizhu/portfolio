% Charlie Zhu
% This code snippit was written by me in 2018. It was originally part of a
% larger subfolder of code, which was done as a collaboration between me
% and a coworker (his code is not included); as such, running the code may
% not entirely work because certain helper functions are not included here.
% PURPOSE: Help user analyze medical ultrasound cineloops, by toggling
% between frames and selecting important points in certain frames. 
% INPUTS: (Originally) the filepath to a folder containing the videos.
% OUTPUTS: (Originally) a .mat file of: the CNR data, the frames selected
% by the user, and the size of the selection.

%% charlie's code
  vid = VideoReader(fullFileName);
  numFrames = vid.NumberOfFrames;
  
  % Two temporary placeholders initialized by garbage values.
  x1 = -10;
  y1 = -10;
  x2 = -50;
  y2 = -50;

  % Initializing.
  currentFrame = 1;
  loopActive = 1;
  
  % Obtaining frame.
  frame = readIndex(vid,currentFrame,fullFileName);
  I = rgb2gray(frame);
  figure(1);
  imshow(I);
  hold on;
  
  % Calibration between screen-sized image and real-life size.
  % if depth is not known for all files manually determine depth and scale 
  if(knownDepth < 1 || knownDepth >5 || mod(knownDepth,1)>0) 
      title('Select 5cm Point (pt 1)');
      [xref_1, yref_1] = ginputc(1, 'Color', 'r');
      title('Select 0cm Point (pt 2)');
      [xref_2, yref_2] = ginputc(1, 'Color', 'b');
      calibratingFactor = abs(yref_2-yref_1)/5;
      disp(['1 cm = ', num2str(calibratingFactor), ' pixels']);
      video(k).scaleFactor = calibratingFactor;

      %title('Select y=0 Point');
      %[x0, y0] = ginputc(1, 'Color', 'r');
      video(k).zeroPoint = yref_2;
      y0 = yref_2;
      
  else %else use avg values for depth and scale 
      
      if(size(I,1) > 900) %video sizes are 1280*960 and 728*800
      
          calibratingFactor = scalesLarge(knownDepth);
          video(k).zeroPoint = zeroPtsLarge(knownDepth);
          y0 = zeroPtsLarge(knownDepth);
          
      else
          
          calibratingFactor = scalesSmall(knownDepth);
          video(k).zeroPoint = zeroPtsSmall(knownDepth);
          y0 = zeroPtsSmall(knownDepth);
      
      end
      video(k).scaleFactor = calibratingFactor;
      
  end
  
  % Allowing user to interact with the video frames.
  title('Select Needle Entrance (Left Click). Exit (Right Click)');
  state = 1; %finding needle entry 
  %state = 2; %finding needle exit
  %state = 3; %finding CNR 
    
  % Looping for all the frames in between the initial and final frames.
  while loopActive
     
      frame = readIndex(vid,currentFrame,fullFileName);
      I = rgb2gray(frame);
      figure(1);
      imshow(I);  
      xlabel('Press Keys to Change Frame: Q=-50, W=-10, E=-5, R=-1, U=+1, I=+5, O=+10, P=+50');
      
      if state~=4 %prevent code from requiring two clicks on needle exit
        [x,y,button] = ginputc(1, 'Color', 'm', 'LineWidth', 1);
      end 
      
      %first evaluate to see if frame needs to change
      if (button == 113)     %q
          currentFrame = currentFrame - 50;
      elseif (button == 119) %w
          currentFrame = currentFrame - 10;
      elseif (button == 101) %e
          currentFrame = currentFrame - 5;
      elseif (button == 114) %r
          currentFrame = currentFrame - 1;
      elseif (button == 112) %p
          currentFrame = currentFrame + 50;
      elseif (button == 111) %o
          currentFrame = currentFrame + 10;
      elseif (button == 105) %i
          currentFrame = currentFrame + 5;
      elseif (button == 117) %u
          currentFrame = currentFrame + 1;
      end 
      
      %ensure index stays within bounds
      if (currentFrame > numFrames)
          currentFrame = numFrames;
      end
      
      if (currentFrame < 1)
          currentFrame = 1;
      end
      
      %else evaluate to see if selection was made
      if state == 1 %find needle entry/exit         
          title('Select Needle Entrance (Left Click). Exit (Right Click)');
          if(button == 1) %left click is selection
              state = 2;
              video(k).needleEnter = (y-y0)/calibratingFactor; 
              video(k).enterFrame = currentFrame;
              title('Select Needle Exit (Left Click). Previous (Right Click)');
          elseif button == 3 %right click is exit
              close all;
              return;       
          end
        
      elseif state == 2
          title('Select Needle Exit (Left Click). Previous (Right Click)');        
          if(button == 1) %left click is selection
              state = 3;
              video(k).needleExit = (y-y0)/calibratingFactor;
              video(k).exitFrame = currentFrame;
              video(k).needleRange = video(k).needleExit - video(k).needleEnter;
              title('Select Frame for CNR (Left Click). Previous (Right Click)');
          elseif button == 3 %right click is exit
              state = 1;
              title('Select Needle Entrance (Left Click). Exit (Right Click)');
          end
          
      elseif state == 3 %select frame for CNR
          
          title('Select Frame for CNR (Left Click). Previous (Right Click)');
          if button == 1
            state = 4;
          elseif button == 3
            state = 2; 
            title('Select Needle Exit (Left Click). Previous (Right Click)');    
          end
          
      elseif state == 4 %find CNR
          hold on;
          
          video(k).CNRFrame = currentFrame;
          
          title('Needle CNR: Select Needle');
          [avg_needle, stdev_needle, ndlPixels] = CNR_Ellipse_Bck4_charlie(I);
          title('Needle CNR: Select Background');
          [avg_bgnd, stdev_bgnd, bkPixels] = CNR_Ellipse_Bck3(I);

          CNR = (avg_needle-avg_bgnd)/stdev_bgnd;
          title(strcat('SNR = ',num2str(CNR,2),': ',fullFileName));
          fig = handle2struct(figure(1));

          [pathstr, name, ext] = fileparts(fullFileName);
          save(strcat(pathstr,'\Analyzed\graphics\',name,'.fig'),'fig');
          saveas(figure(1),strcat(pathstr,'\Analyzed\graphics\',name,'.png'));
          video(k).CNR = CNR;
          video(k).ndlPix = ndlPixels(1); %tracks size of selected regions for the sake of consistency
          video(k).bkPix = bkPixels(1);
          video(k).ndlAvg = avg_needle;
          video(k).bckAvg = avg_bgnd;
          video(k).ndlStdDev = stdev_needle;
          video(k).bckStdDev = stdev_bgnd;
          
          close all; %clear figures
          
          state = 1;
          loopActive = 0;
      end
      
  end