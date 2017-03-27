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
            % 25, 'BEG';
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
                % 30, 'beg';
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
        
        subjFiles = dir('*.cha');
        subjFiles(strncmp('.', {subjFiles.name}, 1)) = []; % remove hidden directories
        subjFiles([subjFiles(:).isdir]) = []; % remove any directories that might be in this directory
        
        for file = 1:length(subjFiles)
            disp([mat2str(round(file/length(subjFiles) * 100, 2)), '%']); % progress counter
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
                goToLine = line; % need an extra variable because we used this to check the next line but don't want to break the loop
                currentLine = text{:}(goToLine);
                
                if strncmp(currentLine, '*PAR', 4)
                    lineCount = lineCount + 1;
                    overallLine = cell(6,1);
                    overallLine{1} = strcat(subjID, '_', num2str(lineCount), '_', storyID);
                    
                    %% looking within a set of *PAR, %mor, %gra lines
                    inPar = 1; 
                    while inPar == 1
                        word = [];
                        morph = {}; 
                        morph_coded = [];
                        grams = {}; 
                        gram_coded = [];
                                    
                        %% pull out the words from the *PAR lines
                        word_count = 0;
                        
                        inParLines = 1;
                        while inParLines == 1
                            currentLine = text{:}(goToLine);
                            currentLine_split = strsplit(currentLine{:}, {' ', '\t'});
                            
                            if word_count > 0 && sum(strncmp(currentLine, {'*', '@', '%'}, 1)) > 0
                                inParLines = 0;
                                break;
                                % disp('end');
                            end

                            for x = 1:length(currentLine_split)
                                try % if, for some reason, there isn't a 1st character present in a cell
                                    if isstrprop(currentLine_split{x}(1), 'punct') 
                                        continue;
                                    end
                                catch
                                    continue;
                                end
                                %Oh and we ALSO need to ignore a
                                %word if it PRECEEDS a '[:' because
                                %the transcript only takes the word
                                %within the [: word]
                                if(x<length(currentLine_split)) %we're not at the end yet AND
                                    if(strcmp(currentLine_split{x+1},'[:')) %the next word is '[:', meaning it's gonna replace this one
                                        continue;
                                    end
                                end
                                
                                currentWord = [];
                                for y = 1:length(currentLine_split{x})
                                    if isstrprop(currentLine_split{x}(y), 'punct')
                                        punctOK = 0; %not okay to have punct in the word
                                        %BUT WAIT. IF
                                        if(y==length(currentLine_split{x})) %this is the last character AND
                                           if(strcmp(currentLine_split{x}(y), ']')) %it's a ']' AND
                                                if(x>1) %this word has a word before it AND
                                                    if(strcmp(currentLine_split{x-1},'[:')) %that word is a '[:', THEN
                                                       punctOK = 1; %we will keep this word even though it has punct in it
                                                    end
                                                end
                                           end
                                        elseif(strcmp(currentLine_split{x}(y),''''))
                                            currentWord = [currentWord currentLine_split{x}(y)];
                                        end
                                        if(~punctOK)
                                            currentWord = [];
                                            break;
                                        end                                       
                                    elseif isstrprop(currentLine_split{x}(y), 'alpha')
                                        currentWord = [currentWord currentLine_split{x}(y)];
                                    end
                                end

                                %% xxx is used to indicate some sort of gesture or mumbling
                                if strcmp(currentWord,'xxx')
                                    currentWord = [];
                                end
                                % disp(word);

                                if ~isempty(currentWord)
                                    word_count = word_count + 1;
                                    word{word_count} = currentWord;
                                end
                            end
                            
                            goToLine = goToLine + 1;
                            if goToLine > length(text{:})
                                break;
                            end
                        end                        
                  
                        %% pull out the parts of speech from %mor and %gra lines
                        if strncmp(currentLine, '%', 1)
                            inPosLines = 1;
                            morphLine = 0;
                            gramLine = 0;
                            while inPosLines == 1
                                currentLine = text{:}(goToLine);
                                posLine_split = strsplit(currentLine{:}, {' ', '\t', '~'});
                                
                                % check to see if the current line ISN'T a
                                % continuation of the old line
                                if sum(strncmp(currentLine, {'*', '@'}, 1)) > 0
                                    inPosLines = 0;
                                    break;
                                elseif strncmp(currentLine, '%', 1)
                                    morphLine = 0;
                                    gramLine = 0;
                                end
                                
                                if strncmp(posLine_split{1}, '%mor', 4) || morphLine == 1 % is this a morpheme line?
                                    morphLine = morphLine + 1;
                                    
                                    if morphLine == 1 % if this is the first morph line (and not a continuation), then we want to eliminate the first element (%mor)
                                        startingPosition = 2;
                                    else
                                        startingPosition = 1;
                                    end
                                    
                                    for currentPart = startingPosition:length(posLine_split) %loop through all the units
                                        split_posParts = strsplit(posLine_split{currentPart}, '|'); %split the string by the delimiter
                                        %So now I want to also take away
                                        %the stuff before and including the
                                        %# sign
                                        if(strfind(split_posParts{1},'#'))
                                            justPOS = strsplit(split_posParts{1},'#'); %just the part of speech
                                            split_posParts{1} = justPOS{2};
                                        end

                                        if length(split_posParts) < 2
                                            continue;
                                        else
                                            % morph_parts =
                                            % strsplit(split_posParts{1},
                                            % ':'); morph = [morph,
                                            % morph_parts{1}]; a =
                                            % strcmp(morph_parts{1},
                                            % morphology(:,2));
                                            morph = [morph, split_posParts{1}];
                                            a = strcmp(split_posParts{1}, morphology(:,2));
                                            % if sum(a) == 0 % print out
                                            % any  missing morph options
                                            %     disp(split_posParts{1});
                                            % end
                                            morph_coded = [morph_coded, morphology{morphology{strcmp(split_posParts{1}, morphology(:,2))},1}];
                                            %get rid of extra junk in the
                                            %word
                                        end
                                    end
                                elseif strncmp(posLine_split{1}, '%gra', 4) || gramLine == 1 % is this a grammar line?
                                    gramLine = gramLine + 1;
                                    
                                    if gramLine == 1 % if this is the first gram line (and not a continuation), then we want to eliminate the first element (%gra)
                                        startingPosition = 2;
                                    else
                                        startingPosition = 1; 
                                    end
                                    
                                    for currentPart = startingPosition:length(posLine_split)
                                        split_posParts = strsplit(posLine_split{currentPart}, '|');
                                        if length(split_posParts) < 2 || strcmp(split_posParts{3}, 'PUNCT')
                                            continue;
                                        else
                                            grams = [grams, split_posParts{3}];
                                            a = strcmp(split_posParts{3}, grammar(:,2));

                                            if strcmp(split_posParts{3}, 'END')
                                                % error('end found')
                                            end

                                            % if sum(a) == 0 % print out
                                            % any missing gram options
                                            %     disp(split_posParts{3});
                                            % end
                                            gram_coded = [gram_coded, grammar{grammar{strcmp(split_posParts{3}, grammar(:,2))},1}];
                                        end
                                    end
                                end
                                
                                goToLine = goToLine + 1;
                                if goToLine > length(text{:})
                                    break;
                                end
                            end
                        end
                        
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
                        
                        if sum(strncmp(currentLine, {'*', '@'}, 1)) > 0
                            inPar = 0;
                            break;
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
