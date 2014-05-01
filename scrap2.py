from numpy import *

branch_geo = array( [[ 30.1172,  380.9565],
   [37.1818,  381.8124],
   [37.7253,  392.9394],
 [ 233.3616,  434.8795]])

print(branch_geo)

a = branch_geo[1:,:]-branch_geo[0:-1,:] 
print(a)


distances =insert( sqrt(sum(square(a),1)) ,0,0) #euclidian distance between points, pad a zero at the front

ltHalf = where(distances < sum(distances)/2)[0][-1] #index the tuple returned by where, then take the last index for which the condition is still true
print('ltHalf', where(distances < sum(distances)/2)[0][-1])

print(distances)



percentAlong = (sum(distances)/2 - cumsum(distances)[ltHalf])/ distances[ltHalf+1]

x,y = branch_geo[ltHalf,:] + percentAlong * ( branch_geo[ltHalf+1] - branch_geo[ltHalf])


print(x,y)