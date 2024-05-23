% -------------------------------------------------------------------------
% 
% 骷髅打金服,爆率超级高
% -------------------------------------------------------------------------
%%
% parameter initialization

function [current_samples, voltage_samples, product_samples] = simulate_and_record()
    % 创建存储结果的数组
    G = [1000,995,990,985,980];
    T=  [25,24.9,24.8,24,7,24.6];
    
    max_power_times = zeros(100, 1);
    current_samples = zeros(100, 1);
    voltage_samples = zeros(100, 1);
    product_samples = zeros(100, 1);
    
    file_name = 'PVarray_test';
    normal_stop_time = '200';

    for i = 1:5 %循环五次
        % load sim model
        load_system(file_name);

        %设置G
        set_param('PVarray_test/Constant', 'Value', num2str(G(i)));
        set_param('PVarray_test/Constant1', 'Value', num2str(G(i)));
        set_param('PVarray_test/Constant2', 'Value', num2str(G(i)));
        set_param('PVarray_test/Constant3', 'Value', num2str(G(i)));
        set_param('PVarray_test/Constant8', 'Value', num2str(G(i)));
        set_param('PVarray_test/Constant9', 'Value', num2str(G(i)));
        set_param('PVarray_test/Constant10', 'Value', num2str(G(i)));
        set_param('PVarray_test/Constant11', 'Value', num2str(G(i)));
        set_param('PVarray_test/Constant22', 'Value', num2str(G(i)));
        set_param('PVarray_test/Constant18', 'Value', num2str(G(i)));
        set_param('PVarray_test/Constant17', 'Value', num2str(G(i)));
        set_param('PVarray_test/Constant16', 'Value', num2str(G(i)));

        %设置T
        set_param('PVarray_test/Constant7', 'Value', num2str(T(i)));

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
    save(sprintf('result.mat'), 'current_samples', 'voltage_samples', 'product_samples');
end
