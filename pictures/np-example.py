B   = 1
a   = 2

I       = [1,2,3,4]
I1      = [1, 4]
I2      = [2, 3]
i_max   = max(I)
P       = ((1 + (len(I) * B)**(1/a)) / ((i_max - 1)**(-1/a) - i_max**(-1/a)))**a
d_min   = P**(1/a) * ((i_max - 1)**(-1/a) - i_max**(-1/a)) / (1 + (len(I) * B)**(1/a))

print('P        =', P)
print('d_min    =', d_min)
for c, i in enumerate(I):
    print('pos(s_{0}) = (0, {1})'.format(c + 1, (P/i)**(1/a)))
    print('pos(r_{0}) = (0, {1})'.format(c + 1, (P/i)**(1/a) + d_min))

print('pos(s_{0}) = ({1}, 0)'.format(len(I) + 1, (2*P/(B*sum(I)))**(1/a)))
print('pos(s_{0}) = ({1}, 0)'.format(len(I) + 2, -(2*P/(B*sum(I)))**(1/a)))

print("SINR_l_s_{0} = {1}".format(len(I) + 1, (P / (2*P/(B*sum(I))) / sum([P/(P/i) for i in I1]))))
