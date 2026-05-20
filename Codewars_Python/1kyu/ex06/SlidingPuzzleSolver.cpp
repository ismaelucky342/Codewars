#include <iostream>
#include <vector>
#include <queue>
#include <climits> // <- añadir esto
#include <algorithm>
#include <cmath>
#include <limits>

using namespace std;

struct Case {
    int value;
    int y, x;
    bool solved = false;

    vector<Case*> paths;

    int distance = INT_MAX;
    Case* back = nullptr;

    Case(int v = 0) : value(v) {}

    void clear() {
        distance = INT_MAX;
        back = nullptr;
    }

    int distanceTo(Case* other) {
        return abs(y - other->y) + abs(x - other->x);
    }

    void swapWith(Case* other) {
        swap(value, other->value);
        swap(solved, other->solved);
    }
};

struct Compare {
    bool operator()(pair<int, Case*> a, pair<int, Case*> b) {
        return a.first > b.first;
    }
};

class Puzzle {
private:
    vector<vector<Case>> puzzle;
    vector<vector<int>> solvedBoard;

    int height, width;

public:
    vector<int> steps;

    Puzzle(const vector<vector<int>>& array) {
        height = array.size();
        width = array[0].size();

        puzzle.resize(height, vector<Case>(width));
        solvedBoard.resize(height, vector<int>(width));

        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                puzzle[i][j] = Case(array[i][j]);
                puzzle[i][j].y = i;
                puzzle[i][j].x = j;

                solvedBoard[i][j] = 1 + j + width * i;
            }
        }

        solvedBoard[height - 1][width - 1] = 0;

        // Build adjacency
        for (int i = 0; i < height; i++) {
            for (int j = 0; j < width; j++) {
                auto& c = puzzle[i][j];

                if (i > 0)
                    c.paths.push_back(&puzzle[i - 1][j]);
                if (i < height - 1)
                    c.paths.push_back(&puzzle[i + 1][j]);
                if (j > 0)
                    c.paths.push_back(&puzzle[i][j - 1]);
                if (j < width - 1)
                    c.paths.push_back(&puzzle[i][j + 1]);
            }
        }
    }

    void clearAll() {
        for (auto& row : puzzle)
            for (auto& c : row)
                c.clear();
    }

    Case* findNumber(int num) {
        for (auto& row : puzzle)
            for (auto& c : row)
                if (c.value == num)
                    return &c;

        return nullptr;
    }

    Case* bestAdjacent(Case* objective, Case* relative) {
        vector<pair<int, Case*>> candidates;

        for (auto path : objective->paths) {
            if (!path->solved) {
                candidates.push_back({
                    relative->distanceTo(path),
                    path
                });
            }
        }

        sort(candidates.begin(), candidates.end(),
             [](auto& a, auto& b) {
                 return a.first < b.first;
             });

        return candidates[0].second;
    }

    vector<Case*> astar(
        Case* start,
        Case* objective,
        Case* forbidden,
        vector<Case*> ignore = {}
    ) {
        priority_queue<
            pair<int, Case*>,
            vector<pair<int, Case*>>,
            Compare
        > pq;

        start->distance = 0;
        pq.push({0, start});

        while (!pq.empty()) {
            auto [_, current] = pq.top();
            pq.pop();

            if (current == objective)
                break;

            for (auto next : current->paths) {
                
                bool ignored = false;

                for (auto ig : ignore) {
                    if (next == ig) {
                        ignored = true;
                        break;
                    }
                }

                if (ignored)
                    continue;

                if (next != forbidden &&
                    !next->solved &&
                    next->distance > current->distance + 1) {

                    next->distance = current->distance + 1;
                    next->back = current;

                    pq.push({
                        next->distance + next->distanceTo(objective),
                        next
                    });
                }
            }
        }

        vector<Case*> path;

        Case* node = objective;

        while (node) {
            path.push_back(node);
            node = node->back;
        }

        reverse(path.begin(), path.end());

        clearAll();

        return path;
    }

    void solveNumber(
        Case* position,
        int number,
        vector<Case*> ignore = {},
        bool markSolved = true
    ) {
        while (position->value != number) {

            Case* origin = findNumber(0);
            Case* objective = findNumber(number);

            Case* adjacent =
                bestAdjacent(objective, position);

            auto path =
                astar(origin, adjacent, objective, ignore);

            for (size_t i = 0; i + 1 < path.size(); i++) {
                steps.push_back(path[i + 1]->value);
                path[i]->swapWith(path[i + 1]);
            }

            steps.push_back(objective->value);
            path.back()->swapWith(objective);
        }

        if (markSolved)
            position->solved = true;
    }

    void lookLine(
        vector<Case*> line,
        vector<int> solutions,
        vector<Case*> helper
    ) {

        for (size_t i = 0; i < line.size() - 2; i++) {
            solveNumber(line[i], solutions[i]);
        }

        solveNumber(helper[2], solutions.back(), {}, false);
        solveNumber(helper[3], solutions[solutions.size()-2], {}, false);

        solveNumber(line[line.size()-1],
                    solutions[solutions.size()-2],
                    {}, false);

        solveNumber(helper[0],
                    solutions.back(),
                    {}, false);

        if (line[line.size()-2] != findNumber(0)) {

            solveNumber(
                helper[1],
                line[line.size()-2]->value,
                {helper[0], line.back()},
                false
            );
        }

        solveNumber(
            line[line.size()-2],
            solutions[solutions.size()-2]
        );

        solveNumber(
            line.back(),
            solutions.back()
        );
    }

    void reduceProblem() {

        for (int i = 0; i < height - 2; i++) {

            vector<Case*> rowLine;
            vector<int> rowSolutions;

            for (int j = 0; j < width; j++) {
                rowLine.push_back(&puzzle[i][j]);
                rowSolutions.push_back(solvedBoard[i][j]);
            }

            vector<Case*> helper1 = {
                &puzzle[i+1][width-1],
                &puzzle[i+1][width-2],
                &puzzle[i+2][width-1],
                &puzzle[i+2][width-2]
            };

            lookLine(rowLine, rowSolutions, helper1);

            vector<Case*> colLine;
            vector<int> colSolutions;

            for (int j = i+1; j < height; j++) {
                colLine.push_back(&puzzle[j][i]);
                colSolutions.push_back(solvedBoard[j][i]);
            }

            vector<Case*> helper2 = {
                &puzzle[height-1][i+1],
                &puzzle[height-2][i+1],
                &puzzle[height-1][i+2],
                &puzzle[height-2][i+2]
            };

            lookLine(colLine, colSolutions, helper2);
        }
    }

    void solve() {

        for (int i = 0; i < 24; i++) {

            bool solved = true;

            int expected = 1;

            for (int y = height - 3; y < height; y++) {
                for (int x = width - 3; x < width; x++) {

                    if (y == height - 1 && x == width - 1) {

                        if (puzzle[y][x].value != 0)
                            solved = false;
                    }
                    else {

                        if (puzzle[y][x].value != expected)
                            solved = false;

                        expected++;
                    }
                }
            }

            if (solved)
                return;

            Case* objective = findNumber(0);
            Case* boardPiece = nullptr;

            if (i < 12) {
                if (objective->y == height-1 && objective->x == width-1)
                    boardPiece = &puzzle[height-2][width-1];

                if (objective->y == height-2 && objective->x == width-1)
                    boardPiece = &puzzle[height-2][width-2];

                if (objective->y == height-2 && objective->x == width-2)
                    boardPiece = &puzzle[height-1][width-2];

                if (objective->y == height-1 && objective->x == width-2)
                    boardPiece = &puzzle[height-1][width-1];
            } else {

                if (objective->y == height-1 && objective->x == width-1)
                    boardPiece = &puzzle[height-1][width-2];

                if (objective->y == height-2 && objective->x == width-1)
                    boardPiece = &puzzle[height-1][width-1];

                if (objective->y == height-2 && objective->x == width-2)
                    boardPiece = &puzzle[height-2][width-1];

                if (objective->y == height-1 && objective->x == width-2)
                    boardPiece = &puzzle[height-2][width-2];
            }

            steps.push_back(boardPiece->value);
            objective->swapWith(boardPiece);
        }
    }

    void solver() {
        reduceProblem();
        solve();
    }
};

vector<int> slide_puzzle(const vector<vector<int>>& array) {
    Puzzle p(array);
    p.solver();
    return p.steps;
}

/*int main() {

    vector<vector<int>> simpleExample = {
        {1, 2, 3, 4},
        {5, 0, 6, 8},
        {9,10, 7,11},
        {13,14,15,12}
    };

    auto result = slidePuzzle(simpleExample);

    for (int move : result)
        cout << move << " ";

    cout << endl;

    return 0;
}*/