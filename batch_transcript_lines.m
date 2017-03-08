%% HARD CODED VARIABLES
extension = '.cha';
stories = {'Sandwich'; 'Cinderella'};
grammar =  {1, 'SUBJ';
            1, 'ESUBJ';
            1, 'CSUBJ';
            1, 'XSUBJ';
            2, 'OBJ';
            2, 'OBJ2'; 
            2, 'IOBJ'; 
            2, 'POBJ';
            3, 'COMP';
            4, 'XCOMP';
            5, 'PRED';
            5, 'CPRED'; 
            5, 'XPRED';
            6, 'JCT';
            7, 'CJCT';
            8, 'XJCT';
            9, 'NJCT';
            10, 'CONJ';
            11, 'MOD';
            12, 'CMOD';
            13, 'XMOD';
            14, 'AUX';
            15, 'NEG';
            16, 'DET';
            17, 'QUANT';
            18, 'PTL';
            19, 'CPZR';
            20, 'COM';
            21, 'INF';
            22, 'COORD';
            23, 'ROOT';
            24, 'LINK';
            25, 'BEG';
            26, 'BEGP';
            27, 'INCROOT';
            28, 'POSTMOD';
            29, 'CPOBJ';
            30, 'END'
            31, 'ENDP'
            32, 'OM'
            33, 'ENUM'
            34, 'LP'
            35, 'POSS'
            36, 'PQ'
            37, 'APP'
            38, 'SRL'
            39, 'L2'
            40, 'DATE'
            };   
morphology =   {1, 'adj';
                2, 'adv';
                3, 'co';
                4, 'conj';
                5, 'conj:coord';
                6, 'conj:subord';
                7, 'conj:prag';
                8, 'det';
                9, 'det:num';
                10, 'det:poss';
                11, 'inf';
                12, 'n';
                13, 'n:prop';
                14, 'n:adv';
                15, 'ptl';
                16, 'prep';
                17, 'pro';
                18, 'pro:refl';
                19, 'pro:poss';
                20, 'pro:dem';
                21, 'pro:indef';
                22, 'pro:exist';
                23, 'pro:per';
                24, 'pro:sub';
                25, 'qn';
                26, 'v';
                27, 'part';
                28, 'aux';
                29, 'coord';
                30, 'beg';
                31, 'mod';
                32, 'cop';
                33, 'step#n';
                34, 'on';
                35, 'neg';
                36, 'neo';
                37, 'det:art';
                38, 'pro:obj';
                39, 'adv:tem';
                40, 'pro:int';
                41, 'pro:rel';
                42, 'det:dem';
                43, 'adv:int';
                44, 'det:int';
                45, 'mod:aux';
                46, 'post';
                47, 'n:gerund';
                48, 'n:let'
                49, 'cm'
                50, 'n:pt'
                51, 'end'
                52, 'uni'
                53, 'bab'
                54, 'sing'
                55, 'bq'
                56, 'meta'
                57, 'eq'
                58, 'adj:pred'   
                59, 'n:adj'
                60, '0aux'
                61, '0n'
                62, 'none'
                63, 'L2'
                };

%% BATCH SCRIPT
% select directory containing the story folders
dataDir = uigetdir();
cd(dataDir);


for story = 1:length(stories)
    disp(stories{story});
    cd(stories{story});
    
    groupDirs = dir();
    groupDirs(strncmp('.', {groupDirs.name}, 1)) = []; % remove hidden directories
    groupDirs(~[groupDirs(:).isdir]) = [];
     
    for group = 1:length(groupDirs)
        disp(groupDirs(group).name);
        cd(groupDirs(group).name)
        
        subjFiles = dir();
        subjFiles(strncmp('.', {subjFiles.name}, 1)) = []; % remove hidden directories
        subjFiles([subjFiles(:).isdir]) = []; % remove any directories that might be in this directory
        
        for file = 1:length(subjFiles)
            disp(file/length(subjFiles));
            fileID = fopen(subjFiles(file).name, 'r');
            text = textscan(fileID, '%s', 5000, 'Delimiter', '\n');
            fclose(fileID);
            
            wordsFile=fopen([subjFiles(file).name(1:end-4) '_words.csv'],'wt');
            graFile=fopen([subjFiles(file).name(1:end-4) '_gra.csv'],'wt');
            morFile=fopen([subjFiles(file).name(1:end-4) '_mor.csv'],'wt');

            subjID = strsplit(subjFiles(file).name, {'_', '.'});
            storyID = subjID(2);
            subjID = subjID(1);
            lineCount = 0;
            
            for line = 1:length(text{:})
                currentLine = text{:}(line);
                
                if strncmp(currentLine, '*PAR', 4)
                    lineCount = lineCount + 1;
                    overallLine = cell(6,1);
                    overallLine{1} = strcat(subjID, '_', num2str(lineCount), '_', storyID);
                    
                    inPar = 1; 
                    goDownLine = 0;
                    while inPar == 1
                        
                        goDownLine = goDownLine + 1;
                        nextLine = text{:}(line+goDownLine);
                        
                        if strncmp(nextLine, '*', 1) || strncmp(nextLine, '@', 1)
                            inPar = 0;
                            continue;
                        elseif strncmp(nextLine, '%', 1)
                            inPos = 1;
                            posLine = nextLine;
                            checkNextLine = 0; 
                            
                            while inPos == 1
                                checkNextLine = checkNextLine + 1;
                                next_nextLine = text{:}(line+goDownLine+checkNextLine);
                                
                                if strncmp(next_nextLine, '*', 1) || strncmp(next_nextLine, '%', 1) || strncmp(next_nextLine, '@', 1)
                                    inPos = 0;
                                    % continue;
                                else
                                    posLine = strcat(posLine, {' '}, next_nextLine);
                                end
                            end
                            
                            % if strncmp(nextLine, '%gra', 4) || strncmp(nextLine, '%mor', 4)
                            %     posLine = nextLine;
                            % else
                            %     posLine = strcat(posLine, ' ', nextLine);
                            % end
                        else
                            continue;
                        end
                        
                        
                        posParts = strsplit(posLine{:}, {' ', '\t'});
                        if strncmp(posParts{1}, '%mor', 4); %if this is a morpheme line
                            morph = {};
                            morph_coded = [];
                            word = {};
                            
                            for currentPart = 2:length(posParts) %loop through all the units
                                split_posParts = strsplit(posParts{currentPart}, '|'); %split the string by the delimiter
                                %So now I want to also take away the stuff
                                %before and including the # sign
                                if(strfind(split_posParts{1},'#'))
                                    justPOS = strsplit(split_posParts{1},'#'); %just the part of speech
                                    split_posParts{1} = justPOS{2};
                                end
                                
                                if length(split_posParts) < 2
                                    continue;
                                else
                                    % morph_parts = strsplit(split_posParts{1}, ':');
                                    % morph = [morph, morph_parts{1}];
                                    % a = strcmp(morph_parts{1},
                                    % morphology(:,2));
                                    morph = [morph, split_posParts{1}];
                                    a = strcmp(split_posParts{1}, morphology(:,2));
                                    if sum(a) == 0
                                        disp(split_posParts{1});
                                    end
                                    morph_coded = [morph_coded, morphology{morphology{strcmp(split_posParts{1}, morphology(:,2))},1}];
                                    %get rid of extra junk in the word
                                    thisWord = split_posParts{2};     
                                    while(strfind(thisWord, '&'))
                                        thisWord = strsplit(split_posParts{2},'&');  
                                        thisWord = thisWord{1};
                                    end
                                    if(strfind(thisWord,'-'))
                                        thisWord = strsplit(split_posParts{2},'-');
                                        thisWord = thisWord{1};
                                    end
                                    if(strfind(thisWord,'~'))
                                        thisWord = strsplit(split_posParts{2},'~');
                                        thisWord = thisWord{1};
                                    end       
                                    if(strcmp(thisWord,'beg') ... 
                                        || strcmp(thisWord,'cm'))
                                        thisWord = [];
                                    end
                                    word = [word, thisWord];
                                end
                            end
                            
                        elseif strncmp(posParts{1}, '%gra', 4)
                            grams = {};
                            gram_coded = [];
                            
                            for currentPart = 2:length(posParts)
                                split_posParts = strsplit(posParts{currentPart}, '|');
                                if length(split_posParts) < 2 || strcmp(split_posParts{3}, 'PUNCT')
                                    continue;
                                else
                                    grams = [grams, split_posParts{3}];
                                    a = strcmp(split_posParts{3}, grammar(:,2));
                                    
                                    if strcmp(split_posParts{3}, 'END')
 %                                       pause;
                                        % error('end found')
                                    end
                                    
                                    if sum(a) == 0
                                        disp(split_posParts{3});
                                    end
                                    gram_coded = [gram_coded, grammar{grammar{strcmp(split_posParts{3}, grammar(:,2))},1}];
                                end
                            end
                            
                        end
                        
                        % for currentPart = 2:length(posParts)
                        %     split_posParts = strsplit(posParts{currentPart}, '|');
                        %     if length(split_posParts) == 2
                        %         morph = [morph, split_posParts{1}];
                        %         morph_coded = [morph_coded, morphology{morphology{strcmp(split_posParts{1}, morphology(:,2))},1}];
                        %         word = [word, split_posParts{2}];
                        %     elseif length(split_posParts) == 3
                        %         if ~strcmp(split_posParts{3}, 'PUNCT')
                        %             grams = [grams, split_posParts{3}];
                        %             gram_coded = [gram_coded, grammar{grammar{strcmp(split_posParts{3}, grammar(:,2))},1}];
                        %         end
                        %     end
                        % end
                        
                        if exist('word', 'var')
                            overallLine{2} = word;
                        end

                        if exist('morph', 'var')
                            overallLine{3} = morph;
                            overallLine{4} = morph_coded;
                        end
                        
                        if exist('grams', 'var')
                            overallLine{5} = grams;
                            overallLine{6} = gram_coded;
                        end
                        
                    end
                    
                    eval(sprintf('lines.%s = overallLine(:);', overallLine{1}{1}));
                    % clear word morph morph_coded grams gram_coded overallLine
                    %add in so it is a blank line when there are no words
                    if(~isempty(overallLine{2}))
                        joint = strjoin(overallLine{2},','); %add commas so it can go into a csv
                        fprintf(wordsFile,joint,'delimiter',',','-append');
                    end
                    fprintf(wordsFile,'\n');
                    if(~isempty(overallLine{4}))
                        stringify = num2str(overallLine{4});
                        stringify = strsplit(stringify);
                        joint = strjoin(stringify,',');
                        fprintf(morFile,joint,'delimiter',',','-append');
                    end
                    fprintf(morFile,'\n');
                    if(~isempty(overallLine{6}))
                        stringify = num2str(overallLine{6});
                        stringify = strsplit(stringify);
                        joint = strjoin(stringify,',');
                        fprintf(graFile,joint,'delimiter',',','-append');
                    end
                    fprintf(graFile,'\n');

                end
                
            end
            fclose(wordsFile);
            fclose(morFile);
            fclose(graFile);
        end
        
        cd ..
    end
    
    cd ..
end

