function [total_rewards, action_history] = modified_epsilon_greedy_bandit(time_steps)
    k = 10;
    epsilon = 0.1;
    alpha = 0.1;

    q_true = zeros(1, k);
    q_est = zeros(1, k);
    total_rewards = zeros(1, time_steps);
    action_history = zeros(1, time_steps);

    for t = 1:time_steps
        q_true = q_true + normrnd(0, 0.01, 1, k);
        
        if rand < epsilon
            action = randi(k);
        else
            [~, action] = max(q_est);
        end
        
        reward = normrnd(q_true(action), 1);
        q_est(action) = q_est(action) + alpha * (reward - q_est(action));
        
        total_rewards(t) = reward;
        action_history(t) = action;
    end
end
