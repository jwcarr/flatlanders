import analysis

exp = 2

for chain in analysis.chain_codes[exp]:
  for gen in range(1, 11):
    test_triangles = analysis.getTriangles(exp+1, chain, gen, "c")
    training_triangles = analysis.getTriangles(exp+1, chain, gen-1, "d")
    for training_i in range(len(training_triangles)):
      for test_i in range(len(test_triangles)):
        if str(training_triangles[training_i][0]) == str(test_triangles[test_i][0]):
          print "Spot match!", chain, gen, training_i, test_i
          if str(training_triangles[training_i][1]) == str(test_triangles[test_i][1]) and str(training_triangles[training_i][2]) == str(test_triangles[test_i][2]):
            print "-- Second point match!!"
          if str(training_triangles[training_i][1]) == str(test_triangles[test_i][2]) and str(training_triangles[training_i][2]) == str(test_triangles[test_i][1]):
            print "-- Third point match!!!"
