function [J, grad] = costFunctionReg(theta, X, y, lambda)
%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));
n = size(theta, 1);

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta

buf = 0;
for i = 1:m
	buf = buf + (-y(i,:) * log(sigmoid(theta' * X(i,:)')) - (1 - y(i, :)) * log(1 - sigmoid(theta' * X(i,:)')));
end

reg_buf = 0;
for j = 2:n
	reg_buf = reg_buf + (theta(j,1) ^ 2);
end
reg_buf = reg_buf * lambda / (2 * m);
J = (buf / m) + reg_buf;

buf = 0;
j = 1;
for i = 1:m
	buf = buf + (sigmoid(theta' * X(i,:)') - y(i, :)) * X(i, j);
end
grad(j,1) = (buf / m);

for j = 2:n
	buf = 0;
	for i = 1:m
		buf = buf + (sigmoid(theta' * X(i,:)') - y(i, :)) * X(i, j);
	end
	grad(j,1) = (buf / m) + (lambda * theta(j, 1) / m);
end

% =============================================================

end
