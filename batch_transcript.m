%% HARD CODED VARIABLES
tab = sprintf('\t');
formatSpec = '%s';
extension = '.cha';
story = 'Sandwich'; % exactly as it appears in the transcripts

%% BATCH SCRIPT
% select directory containing both the aphasia and control folders
dataDir = uigetdir();
cd(dataDir);

% list the aphasia and control folders and move through them to process
% each file
subDirs = dir();
subDirs(strncmp('.', {subDirs.name}, 1)) = []; % remove hidden directories
subDirs(~[subDirs(:).isdir]) = [];
subDirs(strcmp({subDirs.name}, 'Sandwich')) = [];
subDirs(strcmp({subDirs.name}, 'Cinderella')) = [];

if ~exist(story, 'dir')
    mkdir(story); % create a folder with the same name as the story for outputting the files into
    
    cd(story)
    
    for group = 1:length(subDirs)
        mkdir(subDirs(group).name);
    end
    
    cd ..
end

noStoryFound = {};
noStoryFoundCount = 0;

for group = 1:length(subDirs)
    outputFileDir = strcat(pwd, '/', story, '/', subDirs(group).name);
    cd(subDirs(group).name);
    
    subDirs2 = dir();
    subDirs2(strncmp('.', {subDirs2.name}, 1)) = []; % remove hidden directories
    subDirs2(~[subDirs2(:).isdir]) = []; % only keep folders, remove all else
    
    for fileDir = 1:length(subDirs2)
        cd(subDirs2(fileDir).name);
        fileList = dir('*a.cha');
        fileList(strncmp('.', {fileList.name}, 1)) = []; % remove hidden directories
        
        for file = 1:length(fileList)
            fileID = fopen(fileList(file).name, 'r');
            text = textscan(fileID, '%s', 5000, 'Delimiter', '\n');
            fclose(fileID);
            
            outputFile = fopen([outputFileDir, '/', fileList(file).name(1:end-4), '_', story, extension], 'w');
            
            storyTitle = ['@G:', tab, story];
            
            overallStoryFound = 0;
            storyFound = 0;
            
            %if it doesn't start with a * or a % or a @, it needs to be indented
            for len = 1:length(text{1})
                line = text{1}{len};
                if(strcmp(line,storyTitle)) %if we are at the story title, print it
                   fprintf(outputFile, '%s\n',line); 
                   storyFound = 1;
                   overallStoryFound = 1;
                elseif(~storyFound) %we are not in the story, only print headings
                   if(line(1)=='@')  
                       fprintf(outputFile, '%s\n',line);
                   end
                elseif(storyFound) %we are within the story, print lines formatted properly
                    if(~(line(1)=='%' || line(1)=='*' || line(1)=='@'))
                        line = [tab line];
                    end
                    fprintf(outputFile, '%s\n',line); 
                    if(line(1)=='@') %we reached the end of the story
                        storyFound=0;
                    end
                end
            end
            
            if overallStoryFound == 0
                noStoryFoundCount = noStoryFoundCount + 1;
                noStoryFound{noStoryFoundCount} = fileList(file).name;
                fprintf('%s \n', fileList(file).name);
            end
            
            fclose(outputFile);
        end
        
        cd .. % go back up to the group directory
    end
    
    cd ..
end

save(sprintf('noStoryFound_%s.mat', story), 'noStoryFound', 'noStoryFoundCount'); % save the list of files that didn't contain the story