function [y_test,y_pred] = test()
    %%%读取数据
    data = readcell('data2.xlsx', 'Sheet', 'Sheet1');
    G = cell2mat(data(2:end,[1]));
    T = cell2mat(data(2:end,[2]));
    V = cell2mat(data(2:end,[3]));
    I = cell2mat(data(2:end,[4]));
    num = size(V, 1);
    num_sample = num / 20;
    state = zeros(num_sample, 1);
    
    for i = 1:num_sample
        state(i) = cell2mat(data(2 + (i - 1) * 20, [5]));
    end

    %%%数据处理
    % 参数定义
    Gstc = 1000; % STC下辐照度
    Tstc = 25; % STC下温度
    alpha = 0.0066015; % 短路电流温度系数
    beta = -0.29376; % 开路电压温度系数
    gamma = -0.0033;
    delta = 0.085; % 均为PV设备参数
    Rs = 0.83712; % 串联电阻
    k = 1; % 曲线修正系数
    
    % 数据处理
    deltaI = alpha * (T - Tstc);
    Istc = I + deltaI;
    Vstc = V - beta * (Tstc - T) - deltaI * Rs - k * (Tstc - T) .* Istc;
    Pstc = I .* V * Gstc ./ (G .* (1 + gamma * (T - Tstc)) .* (1 + delta * log(G / Gstc)));
    
    % 归一化:a=0,b=1
    M = [max(Istc); max(Vstc); max(Pstc)];
    m = [min(Istc); min(Vstc); min(Pstc)];
    Istc = (Istc - m(1)) / (M(1) - m(1));
    Vstc = (Vstc - m(2)) / (M(2) - m(2));
    Pstc = (Pstc - m(3)) / (M(3) - m(3));
    
    % 生成完整数据集
    x = zeros(num, 3);
    x(:,1) = Istc;
    x(:,2) = Vstc;
    x(:,3) = Pstc;
    x = reshape(x', [], num_sample);
    x = x';
    y = state;

    % 划分训练/测试集
    id = randperm(num_sample);
    x_train = x(id(1:0.8*num_sample), :);
    y_train = y(id(1:0.8*num_sample), :);
    x_test = x(id(0.8*num_sample+1:end), :);
    y_test = y(id(0.8*num_sample+1:end), :);
    
    % 测试
    theta = readcell('weight.xlsx', 'Sheet', 'Sheet1');
    best_theta = cell2mat(theta(2:end, [1:4]));
    y_pred = zeros(num_sample / 5, 1);
    y_P = sigmf(best_theta' * x_test', [1 0]);
    
    for i = 1:num_sample / 5
        [~, maxp] = max(y_P(:, i));
        y_pred(i) = maxp;
    % y_pred = py.numpy.array(y_pred)
    end
end
