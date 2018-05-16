function varargout = gui_som(varargin)
% GUI_SOM M-file for gui_som.fig
%      GUI_SOM, by itself, creates a new GUI_SOM or raises the existing
%      singleton*.
%
%      H = GUI_SOM returns the handle to a new GUI_SOM or the handle to
%      the existing singleton*.
%
%      GUI_SOM('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in GUI_SOM.M with the given input arguments.
%
%      GUI_SOM('Property','Value',...) creates a new GUI_SOM or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before gui_som_OpeningFunction gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to gui_som_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help gui_som

% Last Modified by GUIDE v2.5 24-Aug-2007 16:46:13

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @gui_som_OpeningFcn, ...
                   'gui_OutputFcn',  @gui_som_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before gui_som is made visible.
function gui_som_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to gui_som (see VARARGIN)

% Choose default command line output for gui_som
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes gui_som wait for user response (see UIRESUME)
% uiwait(handles.figure1);

global white_img;
white_img = ones(1,1,3);
set(handles.input_image_canvas,'HandleVisibility','ON');
axes(handles.input_image_canvas);
image(white_img);
axis equal;
axis tight;
axis off;
set(handles.input_image_canvas,'HandleVisibility','OFF');

global limits;
limits = [0 1 0 1 0 1];

set(handles.scatter,'HandleVisibility','ON');
axes(handles.scatter);
image(white_img);
axis equal;
axis tight;
axis (limits);
set(handles.scatter,'HandleVisibility','OFF');

set(handles.som_scatter,'HandleVisibility','ON');
axes(handles.som_scatter);
image(white_img);
axis equal;
axis tight;
axis (limits);
set(handles.som_scatter,'HandleVisibility','OFF');

% --- Outputs from this function are returned to the command line.
function varargout = gui_som_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in som_button.
function som_button_Callback(hObject, eventdata, handles)
% hObject    handle to som_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    % Attributes and input data
    global X;
    global input_size;
    global limits;
    global first;
    global weights;
    global m;
    global n;
    
    m = str2num(get(handles.x_dimension,'String'));
    set(handles.x_dimension,'Enable','off');
    n = str2num(get(handles.y_dimension,'String'));
    set(handles.y_dimension,'Enable','off');
    at_size = 3;

    % Parameters
    if (first)
        weights = rand(m, n, at_size);
        first = false;
        set(handles.systems_messages,'String','Showing first parameters...');
        % Show initial weights
        set(handles.som_scatter,'HandleVisibility','ON');
        axes(handles.som_scatter);
        plot3(weights(:, :, 1), weights(:, :, 2), weights(:, :, 3), 'r.'); grid;
        axis equal;
        axis tight;
        axis (limits);
        set(handles.som_scatter,'HandleVisibility','OFF');
        pause(1);
    end;
    
    epoch = str2num(get(handles.epoch_edit,'String'));;
    alpha = str2num(get(handles.alpha_edit,'String'));
    max_iterations = str2num(get(handles.max_iterations,'String'));

    for iterations=1:max_iterations
        for l=1:length(X)
            % Distances calculations
            distances = zeros(m, n);
            lower_i = 1;
            lower_j = 1;
            for i=1:m
                for j=1:n
                    for k=1:3
                        distances(i, j) = distances(i, j) + (weights(i, j, k) - X(l, k)) * (weights(i, j, k) - X(l, k));
                    end;
                    if (distances(i, j) < distances(lower_i, lower_j))
                        lower_i = i;
                        lower_j = j;
                    end;
                end;
            end;

            % Weights adjustment
            for i=1:m
                for j=1:n
                    for k=1:3
                        weights(i, j, k) = weights(i, j, k) + alpha * h_gauss(i, j, lower_i, lower_j) * (X(l, k) - weights(i, j, k));
                    end;
                end;
            end;
        end;
        alpha = alpha * epoch;
        set(handles.alpha_edit,'String',num2str(alpha));

        global limits;
        set(handles.som_scatter,'HandleVisibility','ON');
        axes(handles.som_scatter);
        plot3(weights(:, :, 1), weights(:, :, 2), weights(:, :, 3), 'r.'); grid;
        axis equal;
        axis tight;
        axis (limits);
        set(handles.som_scatter,'HandleVisibility','OFF');

        set(handles.systems_messages,'String',['Iteration ', num2str(iterations)]);
        pause(0.01);
    end;
    set(handles.systems_messages,'String','SOM Generated! Click on Classify button, or perform more iterations, clicking SOM again. To start a new process, click the Open button.');
    set(handles.classify_button,'Enable','on');


function x_dimension_Callback(hObject, eventdata, handles)
% hObject    handle to x_dimension (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of x_dimension as text
%        str2double(get(hObject,'String')) returns contents of x_dimension as a double


% --- Executes during object creation, after setting all properties.
function x_dimension_CreateFcn(hObject, eventdata, handles)
% hObject    handle to x_dimension (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function y_dimension_Callback(hObject, eventdata, handles)
% hObject    handle to y_dimension (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of y_dimension as text
%        str2double(get(hObject,'String')) returns contents of y_dimension as a double


% --- Executes during object creation, after setting all properties.
function y_dimension_CreateFcn(hObject, eventdata, handles)
% hObject    handle to y_dimension (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function max_iterations_Callback(hObject, eventdata, handles)
% hObject    handle to max_iterations (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of max_iterations as text
%        str2double(get(hObject,'String')) returns contents of max_iterations as a double


% --- Executes during object creation, after setting all properties.
function max_iterations_CreateFcn(hObject, eventdata, handles)
% hObject    handle to max_iterations (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function image_path_Callback(hObject, eventdata, handles)
% hObject    handle to image_path (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of image_path as text
%        str2double(get(hObject,'String')) returns contents of image_path as a double


% --- Executes during object creation, after setting all properties.
function image_path_CreateFcn(hObject, eventdata, handles)
% hObject    handle to image_path (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in open_button.
function open_button_Callback(hObject, eventdata, handles)
% hObject    handle to open_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    image_file = get(handles.image_path,'String');
    file_exists = dir(image_file);
    if (~isempty([file_exists.name]))
    %   Drawing original image
        input_image = double(imread(char(image_file)));
        input_image_int = imread(char(image_file));
        s = size(input_image);
        global W;
        global H;
        global first;
        first = true;
        W = s(1);
        H = s(2);
        set(handles.images_panel,'Title','Input Image');
        set(handles.input_image_canvas,'HandleVisibility','ON');
        axes(handles.input_image_canvas);
        image(input_image_int);
        axis equal;
        axis tight;
        axis off;
        set(handles.input_image_canvas,'HandleVisibility','OFF');

    %   Drawing Scatter Plots
        global R_;
        global G_;
        global B_;
        R_ = reshape(input_image(:, :, 1), 1, W * H); R = [];
        R_ = R_ / max(R_);
        G_ = reshape(input_image(:, :, 2), 1, W * H); G = [];
        G_ = G_ / max(G_);
        B_ = reshape(input_image(:, :, 3), 1, W * H); B = [];
        B_ = B_ / max(B_);
        
        global input_size;
        input_size = length(R_);
        
        sampling = str2num(get(handles.sampling_rate,'String'));
        if (sampling > W || sampling > H)
            sampling = floor(min(W, H) / 2);
            set(handles.sampling_rate,'String', num2str(sampling));
        end;
        
        global X;
        X = [];
        i2 = 1;

        for i=1:sampling:input_size
            R = [R, R_(i)];
            G = [G, G_(i)];
            B = [B, B_(i)];
            X = [X; R(i2), G(i2), B(i2)];
            i2 = i2 + 1;
        end;

        set(handles.scatter,'HandleVisibility','ON');
        axes(handles.scatter);
        plot3(R, G, B, 'r.'); grid;
        axis equal;
        axis tight;
        set(handles.scatter,'HandleVisibility','OFF');

        global white_img;
        global limits;
        set(handles.som_scatter,'HandleVisibility','ON');
        axes(handles.som_scatter);
        image(white_img);
        axis equal;
        axis tight;
        axis (limits);
        set(handles.som_scatter,'HandleVisibility','OFF');

        %   Enabling SOM Button and displaying second message
        set(handles.x_dimension,'Enable','on');
        set(handles.y_dimension,'Enable','on');
        set(handles.som_button,'Enable','on');
        set(handles.epoch_edit,'String','0.99');
        set(handles.alpha_edit,'String','0.9');
        set(handles.classify_button,'Enable','off');
        set(handles.save_button,'Enable','off');
        set(handles.systems_messages,'String','Adjust Input Parameters and click SOM');
    else
        set(handles.systems_messages,'String','Image not found!');
    end;


function sampling_rate_Callback(hObject, eventdata, handles)
% hObject    handle to sampling_rate (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of sampling_rate as text
%        str2double(get(hObject,'String')) returns contents of sampling_rate as a double


% --- Executes during object creation, after setting all properties.
function sampling_rate_CreateFcn(hObject, eventdata, handles)
% hObject    handle to sampling_rate (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end





function alpha_edit_Callback(hObject, eventdata, handles)
% hObject    handle to alpha_edit (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of alpha_edit as text
%        str2double(get(hObject,'String')) returns contents of alpha_edit as a double


% --- Executes during object creation, after setting all properties.
function alpha_edit_CreateFcn(hObject, eventdata, handles)
% hObject    handle to alpha_edit (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end




% --- Executes on button press in classify_button.
function classify_button_Callback(hObject, eventdata, handles)
% hObject    handle to classify_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    % Classifying input image
    global H;
    global W;
    global R_;
    global G_;
    global B_;
    global m;
    global n;
    global weights;
    global output_image;

    output_image = [];
    status = 0;
    increment = 100 / (H * W);
    jump = 3;
    jump_in_jump = jump;
    for p=1:H*W
        lower_i = 1;
        lower_j = 1;
        new_X = double([R_(p), G_(p), B_(p)]);
        distances = zeros(m, n);
        for i=1:m
            for j=1:n
                for k=1:3
                    distances(i, j) = distances(i, j) + (weights(i, j, k) - new_X(k)) * (weights(i, j, k) - new_X(k));
                end;
                if (distances(i, j) < distances(lower_i, lower_j))
                    lower_i = i;
                    lower_j = j;
                end;
            end;
        end;

        output_image(p) = str2num([num2str(lower_i), num2str(lower_j)]);
        status = status + increment;
        if (status > jump_in_jump)
            set(handles.systems_messages,'String',['Classifying input image: ', num2str( floor(status) ), '% done']);
            jump_in_jump = jump_in_jump + jump;
            pause(0.001);
        end
    end;

    set(handles.systems_messages,'String','Classification finished! Click on Save to store this result.');
	set(handles.images_panel,'Title','Classified Image');
    set(handles.save_button,'Enable','on');
    
    output_image = reshape(output_image, W, H);
    set(handles.input_image_canvas,'HandleVisibility','ON');
    axes(handles.input_image_canvas);
    imagesc(output_image);
    axis equal;
    axis tight;
    axis off;
    set(handles.input_image_canvas,'HandleVisibility','OFF');



function epoch_edit_Callback(hObject, eventdata, handles)
% hObject    handle to epoch_edit (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of epoch_edit as text
%        str2double(get(hObject,'String')) returns contents of epoch_edit as a double


% --- Executes during object creation, after setting all properties.
function epoch_edit_CreateFcn(hObject, eventdata, handles)
% hObject    handle to epoch_edit (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end




% --- Executes on button press in save_button.
function save_button_Callback(hObject, eventdata, handles)
% hObject    handle to save_button (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


    set(handles.systems_messages,'String','Saving results...');
    pause(0.01);
    global output_image;
    global W;
    global H;
    
    image_file = get(handles.image_path,'String');
    file_path = dir(image_file);
    image_file = strrep(image_file, file_path.name, ['som_', file_path.name]);
    output_image_rgb = zeros(W, H, 3);
    cm = colormap;
    for i=1:W
        for j=1:H
            output_image_rgb(i, j, :) = cm(output_image(i, j),:);
        end;
    end;
    imwrite(output_image_rgb, image_file);

    file_exists = dir(image_file);
    if (~isempty([file_exists.name]))
        set(handles.systems_messages,'String',['Results saved in ', image_file, ' file.']);
    else
        set(handles.systems_messages,'String','Error when writing file.');
    end;
