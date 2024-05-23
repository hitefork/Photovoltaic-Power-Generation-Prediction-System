    clear all
    close all
    clc

    % 创建存储结果的数组
    data=readcell('data_new.xlsx','Sheet','PSx-u');
    id=1796:1841;
    G=cell2mat(data(id,2));
    T=cell2mat(data(id,3));
    num_tp=size(G,1);
    
    %max_power_times = zeros(100, 1);
    current_samples = zeros(num_tp, 1);
    voltage_samples = zeros(num_tp, 1);
    power_samples = zeros(num_tp, 1);
    
    n_start=20;
    flag=1;
    normal_stop_time = '200';
%     PS_gain=[1,1,1,
%              1,1,1,
%              1,1,1,
%              1,1,1];
    PS_gain=randi([1 3],1,12)*0.3+0.1;
    
    for i = 1:num_tp %循环
        if i>=n_start
            flag=0;
        else
            flag=1;
        end
        if flag==1
            file_name = 'PVarray_normal';
            load_system(file_name);
            %设置G,T
            set_param('PVarray_normal/Constant', 'Value', num2str(G(i)));
            set_param('PVarray_normal/Constant7', 'Value', num2str(T(i)));
        else
            file_name = 'PVarray_PS';
            load_system(file_name);
            %设置G,T
            set_param('PVarray_PS/Constant', 'Value', num2str(G(i)));%OC:8/9,其余0/7
            set_param('PVarray_PS/Constant7', 'Value', num2str(T(i)));
            %设置gain_PS
            set_param('PVarray_PS/Gain11', 'Gain', num2str(PS_gain(1)));
            set_param('PVarray_PS/Gain1', 'Gain', num2str(PS_gain(4)));
            set_param('PVarray_PS/Gain3', 'Gain', num2str(PS_gain(7)));
            set_param('PVarray_PS/Gain10', 'Gain', num2str(PS_gain(10)));

            set_param('PVarray_PS/Gain5', 'Gain', num2str(PS_gain(2)));
            set_param('PVarray_PS/Gain2', 'Gain', num2str(PS_gain(5)));
            set_param('PVarray_PS/Gain', 'Gain', num2str(PS_gain(8)));
            set_param('PVarray_PS/Gain4', 'Gain', num2str(PS_gain(11)));

            set_param('PVarray_PS/Gain9', 'Gain', num2str(PS_gain(3)));
            set_param('PVarray_PS/Gain8', 'Gain', num2str(PS_gain(6)));
            set_param('PVarray_PS/Gain7', 'Gain', num2str(PS_gain(9)));
            set_param('PVarray_PS/Gain6', 'Gain', num2str(PS_gain(12)));
        end
        
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
%         max_power_time = my_current.Time(max_power_index);
%         max_power_times(i) = max_power_time;
        current_samples(i) = my_current.Data(max_power_index);
        voltage_samples(i) = my_voltage.Data(max_power_index);
        power_samples(i) = max_power;

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
    result=cat(2,voltage_samples,current_samples,power_samples);
    %save(sprintf('result.mat'), 'current_samples', 'voltage_samples', 'product_samples');