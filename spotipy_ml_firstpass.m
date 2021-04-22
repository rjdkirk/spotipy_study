% This function will allow me to run this general analysis of a given file,
% assigned to data here, and determine the percentage for the train/test
% split. 

function [accuracy, true, predictions] = spotipy_ml_firstpass(data,split)
% Load raw file with all features
feats = readtable(data);

% Preprocessing
    % Rename Duration_ms
% feats.Properties.VariableNames{14} = 'Duration';

    % Scaling and normalising the data to values between 0 and 1
feats.Brightness = (feats.Brightness - min(feats.Brightness))/(max(feats.Brightness)-min(feats.Brightness));
% feats.Duration = (feats.Duration - min(feats.Duration))/(max(feats.Duration)-min(feats.Duration));
feats.Loudness = (feats.Loudness - min(feats.Loudness))/(max(feats.Loudness)-min(feats.Loudness));
feats.Tempo = (feats.Tempo - min(feats.Tempo))/(max(feats.Tempo)-min(feats.Tempo));

% Split data by category
featsEnergi = feats(feats.Playlist=="Energising",:);
featsRelax = feats(feats.Playlist=="Relaxing",:);
featsSleep = feats(feats.Playlist=="Sleep",:);

% Partition into train/test sets, using p to set the HoldOut rate
p = split;

Ecv = cvpartition(size(featsEnergi,1),'HoldOut',p);
Etrain = featsEnergi(Ecv.training,:);
Etest = featsEnergi(Ecv.test,:);

Rcv = cvpartition(size(featsRelax,1),'HoldOut',p);
Rtrain = featsRelax(Rcv.training,:);
Rtest = featsRelax(Rcv.test,:);

Scv = cvpartition(size(featsSleep,1),'HoldOut',p);
Strain = featsSleep(Scv.training,:);
Stest = featsSleep(Scv.test,:);

% Recombine for complete train/test sets
featsTrain = [Etrain; Rtrain; Strain];
featsTest = [Etest; Rtest; Stest];

% Fit model
knnmodel = fitcknn(featsTrain,"Playlist");

% Test model
predictions = predict(knnmodel,featsTest);
    % Have to change this
predictions = categorical(predictions);
    % Calculate accuracy
iscorrect = predictions==featsTest.Playlist;
accuracy = sum(iscorrect)/numel(iscorrect);
    % For misclassification
isnotcorrect = predictions~=featsTest.Playlist;
misclassrate = sum(isnotcorrect)/numel(isnotcorrect);

    % Confusion matrix - had to change type of featsTest.Playlist
featsTest.Playlist = categorical(featsTest.Playlist);
true = featsTest.Playlist;
    % Leaving here for now
% cm = confusionchart(true,predictions);
% cm.RowSummary = 'row-normalized';
% cm.ColumnSummary = 'column-normalized';
end
