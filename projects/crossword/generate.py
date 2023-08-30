import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for domain in self.domains.keys():
            toRemove = []
            for value in self.domains[domain]:
                if domain.length != len(value):
                    toRemove.append(value)
            for value in toRemove:
                self.domains[domain].remove(value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]

        if overlap is None:
            return False
        else:
            toRemove = []

            i = overlap[0]
            j = overlap[1]
            
            for X in self.domains[x]: 
                for Y in self.domains[y]:
                    if X[i] == Y[j]:
                        break
                else:
                    toRemove.append(X)
                    revised = True

            for word in toRemove:
                self.domains[x].remove(word)    

            return revised            

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = []

        if arcs is None:
            for X in self.domains.keys():
                for Y in self.domains.keys():
                    if X != Y:
                        queue.append((X, Y))
        else:
            for arc in arcs:
                queue.append(arc)

        while len(queue) != 0:

            #dequeuing
            for X, Y in queue:
                queue.remove((X, Y))
            arc = (X, Y)

            if (arc != None):
                X = arc[0]
                Y = arc[1]
                if self.revise(X, Y):
                    if (len(self.domains[X]) == 0):
                        return False
                    for neighbor in self.crossword.neighbors(X):
                        if neighbor != Y:
                            queue.append((neighbor, X))
            else:
                break

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for domain in self.domains.keys():
            if not (domain in assignment.keys()):
                return False
            elif assignment[domain] is None:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        values = []
        for key, value in assignment.items():
            if (value in values):
                return False
            else:
                values.append(value)
            
            if (key.length != len(value)):
                return False

            neighbours = self.crossword.neighbors(key)
            for neighbor in neighbours:
                overlap = self.crossword.overlaps[key, neighbor]
                if neighbor in assignment:
                    if assignment[neighbor][overlap[1]] != value[overlap[0]]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        values = {}
        variables = self.domains[var]
        neighbors = self.crossword.neighbors(var)
        for variable in variables:
            if not (variable in assignment):
                temp = 0
                for neighbor in neighbors:
                    if variable in self.domains[neighbor]:
                        temp = temp + 1
                values[variable] = temp
        
        #sort
        def value(key):
            return values[key]
        return sorted(values, key=value)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        degree = float('-inf')
        value = float('inf')
        for i in self.domains.keys():
            if not (i in assignment):
                if value > len(self.domains[i]):
                    value = len(self.domains[i])
                    variable = i
                    if self.crossword.neighbors(i) is None:
                        degree = 0
                    else:
                        degree = len(self.crossword.neighbors(i))
                elif value == len(self.domains[i]):
                    if self.crossword.neighbors(i) is not None:
                        if degree < len(self.crossword.neighbors(i)):
                            value = len(self.domains[i])
                            variable = i
                            degree = len(self.crossword.neighbors(i))
                        else:
                            variable = i
                            value = len(self.domains[i])
                            degree = 0
        return variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):
            assignment[variable] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(variable)
            
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
