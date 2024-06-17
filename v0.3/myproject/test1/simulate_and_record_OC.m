% -------------------------------------------------------------------------
% 
% 骷髅打金服,爆率超级高
% -------------------------------------------------------------------------
%%
% parameter initialization

function [current_samples, voltage_samples, product_samples,Vstc,Istc,Pstc] = simulate_and_record_OC(my_g,my_t)
    % 创建存储结果的数组

    G=double(py.list(my_g));
    T=double(py.list(my_t));
     
    max_power_times = zeros(length(G), 1);
    current_samples = zeros(length(G), 1);
    voltage_samples = zeros(length(G), 1);
    product_samples = zeros(length(G), 1);
    
    file_name = 'PVarray_OC';
    normal_stop_time = '200';

    for i = 1:length(G) %循环五次

        % load sim model
        load_system(file_name);
        
        %设置G
        set_param('PVarray_OC/Constant8', 'Value', num2str(G(i)));

        %设置T
        set_param('PVarray_OC/Constant9', 'Value', num2str(T(i)));

        % set loading initial operation point off
        set_param(file_name, 'LoadInitialState', 'off');
        set_param(file_name, 'SimscapeUseOperatingPoints', 'off');
        
        % set getting final state on and save it as IniOperPoint
        set_param(file_name, 'SaveCompleteFinalSimState', 'on');
        set_param(file_name, 'SaveFinalState', 'on');
        set_param(file_name, 'FinalStateName', 'myOperPoint');
        
        % 运行模拟并获取结果
        simOut(i) = sim(file_name, 'StopTime', '100');
        my_current = simOut(i).Cur;%都是时序数据
        my_voltage = simOut(i).Volt;
        my_product = simOut(i).Pow;
        

        % 找到最大功率时的索引和数值
        max_power = max(my_product.Data);
        max_power_index = find(my_product.Data == max_power, 1);
    
        % 记录时间、电流、电压和功率值
        max_power_time = my_current.Time(max_power_index);
        max_power_times(i) = max_power_time;
        current_samples(i) = my_current.Data(max_power_index);
        voltage_samples(i) = my_voltage.Data(max_power_index);
        product_samples(i) = max_power;

        % 保存当前状态
        %save(sprintf('IniOperPoint_%d.mat', i), 'my_current', 'my_voltage', 'my_product');
        

        % 设置 loading initial operation point on
        set_param(file_name, 'LoadInitialState', 'on'); 
        set_param(file_name, 'InitialState', 'myOperPoint');
        set_param(file_name, 'SimscapeUseOperatingPoints', 'on'); % enable Operation point initialization
        set_param(file_name, 'SimscapeOperatingPoint', 'myOperPoint');
        
        % 恢复正常的停止时间
        set_param(file_name, 'StopTime', normal_stop_time);
        % 重置模型到初始状态
        close_system(file_name, 0);










    end
    %save(sprintf('result.mat'), 'current_samples', 'voltage_samples', 'product_samples');
    V=voltage_samples;
    I=current_samples;
    P=product_samples;
    V=V';
    I=I';
    P=P';
    %%%数据处理
    %定义参数
    Gstc=1000;%STC下辐照度
    Tstc=25;%STC下温度
    alpha=0.00045;%短路电流温度系数,量纲1/℃
    beta=-0.29376;%开路电压温度系数，量纲V/℃
    gamma=-0.0031;%PV设备参数，量纲1/℃，gamma≈alpha+beta
    delta=0.085;%PV设备参数，量纲1
    Rs=0.83712;%串联电阻
    k=0.04;%曲线修正系数
    %数据处理
    deltaI=alpha*(T-Tstc);
    %Istc=I+deltaI;
    Istc=I./(1+deltaI)./(G/Gstc);
    Vstc=V-beta*(Tstc-T)-deltaI*Rs-k*(Tstc-T).*Istc;
    %Pstc=I.*V*Gstc./(G.*(1+gamma*(T-Tstc)).*(1+delta*log(G/Gstc)));
    Pstc=Vstc.*Istc;

end
