
# 
mA, wid = [35.46, 31.48, 26.49, 23.39, 23.18], 27
# mA, wid = [9.46, 6.48, 4.49, 2.39, 2.18], 5

# mA = [35.45, 34.45, 31.48, 29.48, 26.47, 25.47, 23.90, 22.90, 22.70, 21.70]
print('elements\t\t\t', mA)
print('sum of elements:\t',sum(mA))


print('rounded:\t\t\t', sum([round(el) for el in mA]))

print('pct error:\t\t\t\t{}%'.format( round(100*(sum(mA) - sum([round(el) for el in mA]))/sum(mA), 2)))
decimal = [round(el%1,2) for el in mA]




print( 'decimal portion:\t',decimal)



from numpy import mean, array, floor, ceil


print( 'mean decimal value:\t',mean(decimal))


print('aspect {}:\t\t\t'.format(wid),mean(array(mA) /wid ))


mAr = [ floor(el) if el < mean(decimal) else ceil(el) for el in mA]

print('adjusted array:\t\t', mAr)

print('sum adjusted:\t\t', sum(mAr))

