import utilities.io     as io 
import solutions.day1   as d1 
import solutions.day2   as d2 
import solutions.day3   as d3 
import solutions.day4   as d4 
import solutions.day5   as d5 
import solutions.day6   as d6 
import solutions.day7   as d7 
import solutions.day8   as d8 
import solutions.day9   as d9 
import solutions.day10  as d10
import solutions.day11  as d11
import solutions.day12  as d12
import solutions.day13  as d13
import solutions.day14  as d14
import solutions.day15  as d15
import solutions.day16  as d16
import solutions.day17  as d17
import solutions.day18  as d18
import solutions.day19  as d19
import solutions.day20  as d20
import solutions.day21  as d21
import solutions.day22  as d22
import solutions.day23  as d23
import solutions.day24  as d24
import solutions.day25  as d25 
import time

solutions = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, 
             d16, d17, d18, d19, d20, d21, d22, d23, d24, d25]

def main():
    # If the files need to be generated
    #io.generate_solution_files()
    #return

    print(("-"*23) + "\n- ADVENT OF CODE 2019 -\n" + ("-"*23) + "\n")
    while True:
        try:
            soln = int(input("Choose a day to solve: ")) - 1
            print()
            if soln > 24 or soln < -1:
                raise ValueError
        except:
            print("Invalid input. Choose a solution from 1-25, or 0 to quit.\n")
            continue

        if soln == -1:
            break
        
        start_time = time.time()
        solutions[soln].solve_p1()
        elapsed = time.time() - start_time
        print(f"(Part One took {round(elapsed, 2)} seconds)\n")
        start_time = time.time()
        solutions[soln].solve_p2()
        elapsed = time.time() - start_time
        print(f"(Part Two took {round(elapsed, 2)} seconds)\n")
            


if __name__ == "__main__":
    main()