 clear; clc;

% Open observational data
% %

data = readtable('filtered_table.csv');

% Step 2: Select the columns headed 'lon' and 'lat'
lon_obs = data.Lon;
lat_obs = data.Lat;


% Decide minimum drainage area for your grid points to have
dra_value = 100;


% Open model data from static fields
dra = double(nc_varget('SAMCORDEX_006degree_stk.static_fields.nc','dra'));
dra1=dra;

lat = double(nc_varget('SAMCORDEX_006degree_stk.static_fields.nc','lat'));
lon = double(nc_varget('SAMCORDEX_006degree_stk.static_fields.nc','lon'));



xlon(dra < dra_value) = NaN;
xlat(dra < dra_value) = NaN;
coordinates = [lon_obs(:),lat_obs(:)];
coordinates_model = [reshape(xlon,[numel(xlon) 1]),reshape(xlat,[numel(xlat) 1])];

% Removing drainage area smaller than what was stablished 
discharge(dra < dra_value) = NaN;
dra(dra < dra_value) = NaN;

% % Searching the coordinates
coor = NaN(size(coordinates,1),size(coordinates,2));
pos = NaN(size(coordinates,1),1);
xlat_pos = NaN(size(coordinates,1),1);
xlon_pos = NaN(size(coordinates,1),1);

% Looking for the nearest point
for i=1:size(coordinates,1)
    pos(i) = dsearchn(coordinates_model,coordinates(i,:));
    coor(i,:) = coordinates_model(pos(i),:);
    xlat_pos(i) = find(lat == coor(i,2));
    xlon_pos(i) = find(lon == coor(i,1));
    clear pos
end

lat_model=lat(xlat_pos);
lon_model=lon(xlon_pos);


data.lon_model = lon_model;
data.lat_model = lat_model;

% Step 4: Reorder the columns to make 'lon_model' and 'lat_model' the first two columns
data = [data(:, {'lon_model', 'lat_model'}), data(:, setdiff(data.Properties.VariableNames, {'lon_model', 'lat_model'}))];

% Step 5: Save the modified table to a new CSV file
writetable(data, 'coord_SAM.csv');

% Display the modified table (optional)
disp(data);

