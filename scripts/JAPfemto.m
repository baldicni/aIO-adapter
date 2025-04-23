clear
close all
clc

Opts = Options('Gravity', 9.81 * [0 -1 0]); 
Opts.PlotSettings.Animate = true; 
Opts.PlotSettings.ScaleEigenModes = 0.1;
Opts.PlotSettings.AnimationRepeat = 1;
Opts.PlotSettings.AnimationRepeat =5;

JAP = Assembly('JAP', 'Options', Opts);

%% MARIONETTE %%

WIRE_MA = Beam('WIRE_MA');
WIRE_MA.OrientationVector = [0 -1 0];
WIRE_MA.Length = 0.160;
WIRE_MA.CrossSection = struct('shape', 'circ', 'r', 0.1e-3);
WIRE_MA.Material = 'C70';

MA = Mass('MA');
MA.OrientationVector = [0 -1 0];
MA.CrossSection= struct('shape','circ','r',0.1);
MA.Length = 0.04;
MA.Mass = 2.4;
MA.Inertia = [0.0131 0.0169 0.005243];
MA.Material = 'C70';
MA.PlotObject3D = true;
MA.PlotColor = [0.5, 0.8, 0.5]


SPRING_L = Spring('SPRING_L');
SPRING_L.OrientationVector = [0 -1 0];
SPRING_L.StiffnessMatrix = diag([1e10, 6010, 1e10, 1e10, 1e10, 1e10]);
SPRING_L.Length = 0.01/2;

SPRING_R = Spring('SPRING_R');
SPRING_R.OrientationVector = [0 -1 0];
SPRING_R.StiffnessMatrix = diag([1e10, 6010, 1e10, 1e10, 1e10, 1e10]);
SPRING_R.Length = 0.01/2;

RIG_MA_L = Rigid('RIG_MA_L');
RIG_MA_L.OrientationVector = [1 0 0]; % The z-axis is the beam axis
RIG_MA_L.Length = 0.1;

RIG_MA_R = Rigid('RIG_MA_R');
RIG_MA_R.OrientationVector = [1 0 0]; % The z-axis is the beam axis
RIG_MA_R.Length = 0.1;

%% MIRROR %%

WIRE_L_MI = Beam('WIRE_L_MI');
WIRE_L_MI.OrientationVector = [0 -1 0];
WIRE_L_MI.Length = 0.200;
WIRE_L_MI.CrossSection = struct('shape', 'circ', 'r', 0.58e-3);
WIRE_L_MI.Material = 'C70';

WIRE_R_MI = Beam('WIRE_R_MI');
WIRE_R_MI.OrientationVector = [0 -1 0];
WIRE_R_MI.Length = 0.200;
WIRE_R_MI.CrossSection = struct('shape', 'circ', 'r', 0.58e-3);
WIRE_R_MI.Material = 'C70';

RIG_MI_L = Rigid('RIG_MI_L');
RIG_MI_L.OrientationVector = [1 0 0]; % The z-axis is the beam axis
RIG_MI_L.Length = 0.1;

RIG_MI_R = Rigid('RIG_MI_R');
RIG_MI_R.OrientationVector = [1 0 0]; % The z-axis is the beam axis
RIG_MI_R.Length = 0.1;

MI = Mass('MI','Interesting', true);
MI.OrientationVector = [0 0 1];
MI.CrossSection= struct('shape','circ','r',0.1);
MI.Length = 0.03;
MI.Mass = 2.4;
MI.Inertia = [0.006998 0.005863 0.0011422];
MI.Material = 'C70';
MI.PlotObject3D = true;





JAP.assemble('GND',1,WIRE_MA,1);
JAP.assemble(WIRE_MA,2,MA,1);
JAP.assemble(MA,1,RIG_MA_L,1);
JAP.assemble(MA,1,RIG_MA_R,2);
JAP.assemble(RIG_MA_L,2,SPRING_L,1);
JAP.assemble(RIG_MA_R,1,SPRING_R,1);
JAP.assemble(SPRING_R,2,WIRE_R_MI,1);
JAP.assemble(SPRING_L,2,WIRE_L_MI,1);
JAP.assemble(MI,1,RIG_MI_L,1);
JAP.assemble(MI,1,RIG_MI_R,2);
JAP.assemble(WIRE_L_MI,2,RIG_MI_L,2);
JAP.assemble(WIRE_R_MI,2,RIG_MI_R,1);

% for i=1:10
%     JAP.plot(i)
% end

JAP.Freq

%% SS
range = [-3,2.1,5000]; %test test
f = logspace(range(1), range(2), range(3));
w = 2*pi*f;

SS = JAP.SS;
SSf=full(SS);


Name = 'MI';
desiredPairs = {
    [Name, '_x_o'],  'Ground_x_i';
    [Name, '_y_o'],  'Ground_y_i';
    [Name, '_z_o'],  'Ground_z_i';
    [Name, '_rx_o'], 'Ground_rx_i';
    [Name, '_ry_o'], 'Ground_ry_i';
    [Name, '_rz_o'], 'Ground_rz_i'};

[mag, ~, ~] = bode(SS(unique(desiredPairs(:,1),'stable'), unique(desiredPairs(:,2), 'stable')), w);


XtoX = squeeze(mag(1,1,:));
ZtoZ = squeeze(mag(3,3,:));
RxtoZ = squeeze(mag(3,4,:));


figure
h1 = loglog(f, abs(ZtoZ), 'LineWidth', 1.5, 'Color', 'r'); % Green for ZtoZ * hU
hold on;
h2 = loglog(f, abs(XtoX), 'r', 'LineWidth', 1.5, 'Color','k'); % Red for YtoY * vU
grid on;

title('JAP Horizontal TFs', 'FontSize', 14);
xlabel('Frequency (Hz)', 'FontSize', 12, 'FontWeight', 'bold'); % X-axis label for frequency
ylabel('Strain (1/\surdHz)', 'FontSize', 12, 'FontWeight', 'bold');      % Y-axis label for magnitude
set(gca, 'GridAlpha', 0.3, 'MinorGridAlpha', 0.1, 'FontSize', 12);
set(gca, 'LineWidth', 1, 'FontWeight', 'bold');
legend('Z to Z', 'X to X');%
xlim([min(f), max(f)])
currentYLim = ylim;
ylim([1e-25, currentYLim(2)])
hold off;

h1.ButtonDownFcn = @(src, event) onClick(src, event, PAY, 1);
h2.ButtonDownFcn = @(src, event) onClick(src, event, PAY, 2);

function onClick(~, event, JAP, plotNumber)
    % Get the x-coordinate of the click
    clickX = event.IntersectionPoint(1);
    % Find the closest frequency in ET.Freq to clickX
    [~, idxClicked] = min(abs(JAP.Freq{:,"Frequency [Hz]"} - clickX));
    % Call the desired action with the found index
    fprintf('Plot %d clicked. Calling JAP.plot(%d)\n', plotNumber, idxClicked);
    
    %h = figure(10);
    JAP.plot(idxClicked);
    %close(h);
    
end