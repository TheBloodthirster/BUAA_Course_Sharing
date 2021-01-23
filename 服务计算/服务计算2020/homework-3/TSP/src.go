package main

import (
	"fmt"
	"sync"
)

type Combination struct {
	comb    uint64
	n, k    int
	isFirst bool
}

const MaxUint = ^uint(0)
const MaxUint64 = ^uint64(0)
const goroutineNum = 32

func NewCombination(n, k int) *Combination {
	return &Combination{^(MaxUint64 << k), n, k, true}
}

func (a *Combination) Next() bool {
	if a.isFirst {
		a.isFirst = false
		return true
	}
	left := MaxUint64
	for i := 0; i < a.n-1; i++ {
		if a.comb&3 == 1 {
			a.comb++
			a.comb = a.comb<<i | ^left
			return true
		}
		left <<= a.comb & 1
		a.comb >>= 1
	}
	return false
}

func calc(a *dstMapType, i int, index uint64) {
	a.info[index] = make([]uint, 0, i)
	nodes := make([]uint8, 0, i)
	for k, p := index, 0; k != 0; k, p = k>>1, p+1 {
		if k&1 != 0 {
			nodes = append(nodes, uint8(p))
		}
	}
	if i == 1 {
		a.info[index] = append(a.info[index], a.DstMap[a.N][nodes[0]])
		return
	}
	for k := 0; k < i; k++ {
		minD := MaxUint
		for p, q := 0, 0; p < i-1; p++ {
			if p == k {
				q = 1
			}
			dst := a.info[index&^uint64(1<<nodes[k])][p] + a.DstMap[nodes[p+q]][nodes[k]]
			if minD > dst {
				minD = dst
			}
		}
		a.info[index] = append(a.info[index], minD)
	}

}
func printPath(a *dstMapType, r *result, minD uint) {
	comb := (1 << a.N) - 1
	r.Path = make([]int, a.N+1)
	r.Path[a.N] = a.N
	for i := a.N; comb != 0; i-- {
		for j, k := 0, 0; ; k++ {
			if (comb>>k)&1 == 1 {
				if a.info[comb][j]+a.DstMap[k][r.Path[i]] == minD {
					minD = a.info[comb][j]
					comb &= ^(1 << k)
					r.Path[i-1] = k
					break
				}
				j++
			}
		}
	}
	fmt.Println("path:")
	for i, j, sign := 0, 0, 0; j <= a.N; i, j = (i+1)%(a.N+1), j+sign {
		if r.Path[i] == 0 {
			sign = 1
		}
		if sign == 1 {
			fmt.Printf("V%02d -> V%02d\n", r.Path[i]+1, r.Path[(i+1)%(a.N+1)]+1)
		}
	}
}

func Run(a *dstMapType) {
	a.N--
	a.info = make([][]uint, 1<<a.N)
	sema := make(chan struct{}, goroutineNum)
	var wg sync.WaitGroup
	for i := 1; i <= a.N; i++ {
		comb := NewCombination(a.N, i)
		for comb.Next() {
			sema <- struct{}{}
			wg.Add(1)
			j := comb.comb
			go func() {
				defer wg.Done()
				calc(a, i, j)
				<-sema
			}()
		}
		wg.Wait()
	}
	minD := MaxUint
	for i := 0; i < a.N; i++ {
		dst := a.info[(1<<a.N)-1][i] + a.DstMap[i][a.N]
		if minD > dst {
			minD = dst
		}
	}
	if a.N == 0 {
		minD = a.DstMap[0][0]
	}
	r := result{a.Id, nil, minD}
	fmt.Printf("distance: %d\n", minD)
	printPath(a, &r, minD)
	resultMap[a.Id] = r
}
