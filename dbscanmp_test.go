package dbscan

import (
	"fmt"
	"log"
	"math"
	"testing"
)

type MultiPoint struct {
	position float64
}

func (s MultiPoint) DistanceTo(c Point) float64 {
	distance := math.Abs(c.(MultiPoint).position - s.position)
	return distance
}

func (s MultiPoint) Name() string {
	return fmt.Sprint(s.position)
}

func TestMpPutAll(t *testing.T) {
	testMap := make(map[string]Point)
	clusterList := []Point{
		MultiPoint{10},
		MultiPoint{12},
	}
	merge(testMap, clusterList...)
	mapSize := len(testMap)
	if mapSize != 2 {
		t.Errorf("Map does not contain expected size 2 but was %d", mapSize)
	}
}

//Test find neighbour function
func TestMpFindNeighbours(t *testing.T) {
	log.Println("Executing TestMpFindNeighbours")
	clusterList := []Point{
		MultiPoint{0},
		MultiPoint{1},
		MultiPoint{-1},
		MultiPoint{1.5},
		MultiPoint{-0.5},
	}

	eps := 1.01
	neighbours := findNeighbours(clusterList[0], clusterList, eps)
	if 3 != len(neighbours) {
		t.Error("Mismatched neighbours counts")
	}
}

func TestMpExpandCluster(t *testing.T) {
	log.Println("Executing TestMpExpandCluster")
	expected := 4
	clusterList := []Point{
		MultiPoint{0},
		MultiPoint{1},
		MultiPoint{2},
		MultiPoint{2.1},
		MultiPoint{5},
	}

	eps := 1.0
	minPts := 1
	visitMap := make(map[string]bool)
	cluster := make([]Point, 0)
	cluster = expandCluster(cluster, clusterList, visitMap, minPts, eps)
	if expected != len(cluster) {
		t.Error("Mismatched cluster counts")
	}
}

func TestMpCluster(t *testing.T) {
	clusters := Cluster(2, 1.0,
		MultiPoint{1},
		MultiPoint{0.5},
		MultiPoint{0},
		MultiPoint{5},
		MultiPoint{4.5},
		MultiPoint{4})

	if 2 == len(clusters) {
		if 3 != len(clusters[0]) || 3 != len(clusters[1]) {
			t.Error("Mismatched cluster member counts")
		}
	} else {
		t.Error("Mismatched cluster counts")
	}
}

func TestMpClusterNoData(t *testing.T) {
	log.Println("Executing TestMpClusterNoData")

	clusters := Cluster(3, 1.0)
	if 0 != len(clusters) {
		t.Error("Mismatched cluster counts")
	}
}
