function [] = scatter_plot(filelist)
    % Determine the number of files
    num_files = length(filelist);

    % Calculate the number of rows and columns for the subplot grid
    num_rows = 3;
    num_cols = 5;

    % Create a figure to hold the subplots
    figure

    % Loop through the list of file names
    for i = 1:num_files
        filename = filelist{i};
    
        % Read data from the current CSV file
        data = csvread(filename, 1, 0);
        y_test = data(:, 1);
        y_pred = data(:, 2);
    
        % Initialize variables to track the global maximum values
        global_max_test = -inf;
        global_max_pred = -inf;

        % Update the global maximum values
        global_max_test = max(global_max_test, max(y_test));
        global_max_pred = max(global_max_pred, max(y_pred));

        % Determine the overall axis limit
        axis_limit = ceil(max(global_max_test, global_max_pred) / 500) * 500;

        % Determine appropriate tick interval based on axis_limit
        if i ==8 
            axis_limit = 150;
            tick_interval = 75;
        elseif axis_limit == 500;
            tick_interval = 250;
        elseif axis_limit == 3500
            tick_interval = 3500/2;
        elseif axis_limit == 1500
            tick_interval = 750;
        elseif axis_limit == 1000
            tick_interval = 500;
        elseif axis_limit == 2000
            tick_interval = 1000;
        elseif axis_limit == 3000
            tick_interval = 1500;
        elseif axis_limit == 4000
            tick_interval = 2000;
        elseif axis_limit == 5000
            tick_interval = 2500;
        else
            tick_interval = 500; % default for values greater than 4000
        end

        % Read data from the current CSV file
        data = csvread(filename, 1, 0);
        y_test = data(:, 1);
        y_pred = data(:, 2);

        X = y_test;
        Y = y_pred;
        numbins = 100;

        % Create a 2D histogram of the data
        [values, centers] = hist3([X Y], [numbins numbins]);

        centers_X = centers{1,1};
        centers_Y = centers{1,2};

        binsize_X = abs(centers_X(2) - centers_X(1)) / 2;
        binsize_Y = abs(centers_Y(2) - centers_Y(1)) / 2;
        bins_X = zeros(numbins, 2);
        bins_Y = zeros(numbins, 2);

        for j = 1:numbins
            bins_X(j, 1) = centers_X(j) - binsize_X;
            bins_X(j, 2) = centers_X(j) + binsize_X;
            bins_Y(j, 1) = centers_Y(j) - binsize_Y;
            bins_Y(j, 2) = centers_Y(j) + binsize_Y;
        end

        scatter_COL = zeros(length(X), 1);

        onepercent = round(length(X) / 100);

        for j = 1:length(X)
            if (mod(j, onepercent) == 0)
                fprintf(' ');
            end

            last_lower_X = NaN;
            last_higher_X = NaN;
            id_X = NaN;

            c_X = X(j);
            last_lower_X = find(c_X >= bins_X(:, 1));
            if (~isempty(last_lower_X))
                last_lower_X = last_lower_X(end);
            else
                last_higher_X = find(c_X <= bins_X(:, 2));
                if (~isempty(last_higher_X))
                    last_higher_X = last_higher_X(1);
                end
            end
            if (~isnan(last_lower_X))
                id_X = last_lower_X;
            else
                if (~isnan(last_higher_X))
                    id_X = last_higher_X;
                end
            end

            last_lower_Y = NaN;
            last_higher_Y = NaN;
            id_Y = NaN;

            c_Y = Y(j);
            last_lower_Y = find(c_Y >= bins_Y(:, 1));
            if (~isempty(last_lower_Y))
                last_lower_Y = last_lower_Y(end);
            else
                last_higher_Y = find(c_Y <= bins_Y(:, 2));
                if (~isempty(last_higher_Y))
                    last_higher_Y = last_higher_Y(1);
                end
            end
            if (~isnan(last_lower_Y))
                id_Y = last_lower_Y;
            else
                if (~isnan(last_higher_Y))
                    id_Y = last_higher_Y;
                end
            end

            scatter_COL(j) = values(id_X, id_Y);
        end

        % Create a subplot in the grid layout
        subplot(num_rows, num_cols, i);

        % Create a scatter plot with a color map
        scatter(y_test, y_pred, 20, scatter_COL, '.');
        colormap('jet');
        caxis([0 100]);

        % Calculate R^2
        C = corrcoef(y_test, y_pred);
        R2 = C(1, 2)^2;

        % Add R^2 value to the title
        title(['CL', num2str(i)], 'FontSize', 20);

        % Display axis labels
        xlabel('SWE measurements (mm)', 'FontSize', 13);
        ylabel('SWEML (mm)', 'FontSize', 13);

        % Ensure that all subplots have axis labels
        if i > num_files - num_cols
            xlabel('SWE measurements (mm)', 'FontSize', 13);
        end
        if mod(i, num_cols) == 1
            ylabel('SWEML (mm)', 'FontSize', 13);
        end

        % Display R^2 value on the plot
        text(0.1, 0.9, ['R^2 = ', num2str(round(R2, 2))], 'FontSize', 13, 'Units', 'normalized', 'Color', 'k');

        ax = gca; 
        ax.FontSize = 12;  

        % Set x and y axis limits to be the same
        axis([0 axis_limit 0 axis_limit]);  % Apply the same axis limits for x and y

        % Set x amd y axis ticks to be consistent
        xticks(0:tick_interval:axis_limit);
        yticks(0:tick_interval:axis_limit);

        
        % Add x=y line
        hold on;
        plot([0, axis_limit], [0, axis_limit], '--k');

        hold off;
        cb = colorbar('eastoutside');
        cb.Ticks = 0:20:100;

        tick_labels = arrayfun(@num2str, cb.Ticks, 'UniformOutput', false);
        tick_labels{1} = '1';
        cb.TickLabels = tick_labels;
        title(cb, 'N', 'FontSize', 13);  % Label the colorbar as 'N'

        grid off;
    end

end

fileliest = {'Cl_1.csv', 'Cl_2.csv', 'Cl_3.csv', 'Cl_4.csv', 'Cl_5.csv', 'Cl_6.csv', 'Cl_7.csv', 'Cl_8.csv', 'Cl_9.csv', 'Cl_10.csv', 'Cl_11.csv', 'Cl_12.csv', 'Cl_13.csv'}
scatter_plot(filelist);

fig = gcf;
filename = 'Figure5';
fig.Position = [fig.Position(1) fig.Position(2) 2300 1000];

set(fig, 'PaperPositionMode', 'auto'); 
print(fig, filename, '-dtiff', '-r300');




