        for i in range(self.n):
            if i % 2 == 0:
                sens = 0
            else:
                sens = 1

            # O, start, gap, ampli, sens=0
            self[i] = HalfWave( self.O,
                                points[i][0],
                                points[i][1],
                                self.ampli*0.8**i,
                                sens)

    def get_points(self):
        start = self.start
        gap = self.gap
        points = [  (start + 0   * gap, gap*1),
                    (start + 1   * gap, gap*0.9),
                    (start + 1.9 * gap, gap*0.8),
                    (start + 2.7 * gap, gap*0.7),
                    (start + 3.4 * gap, gap*0.6),
                    (start + 4.0 * gap, gap*0.5),
                    (start + 4.5 * gap, gap*0.4),
                    (start + 4.9 * gap, gap*0.3)  ]
        return points
