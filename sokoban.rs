use std::collections::HashMap;
use std::fmt;

type Vector = (i16, i16);
type BaseBoard = Vec<Vec<char>>;
type Vectors = Vec<Vector>;

fn vec_plus(v1: Vector, v2: Vector) -> Vector {
    (v1.0 + v2.0, v1.1 + v2.1)
}

#[derive(Clone)]
struct Board {
    brd: BaseBoard,
    targets: Vectors,
}

impl Board {
    fn new(baseboard: BaseBoard, targets: Vectors) -> Self {
        Self {
            brd: baseboard,
            targets,
        }
    }

    fn is_valid_move(&self, pos: Vector) -> bool {
        let (x, y) = pos;
        x >= 0 && x < self.brd.len() as i16 && y >= 0 && y < self.brd[0].len() as i16 && self.brd[x as usize][y as usize] != '#'
    }

    fn find_children(&self) -> Vec<Board> {
        let mut children = vec![];
        let (pos, _) = self.find_OoIs();
        let directions: HashMap<char, Vector> = [
            ('U', (-1, 0)),
            ('D', (1, 0)),
            ('L', (0, -1)),
            ('R', (0, 1)),
        ].iter().cloned().collect();

        for (_, dir) in &directions {
            let new_pos = vec_plus(pos, *dir);

            if self.is_valid_move(new_pos) {
                let mut new_brd = self.brd.clone();
                if new_brd[new_pos.0 as usize][new_pos.1 as usize] == 'X' {
                    let block_new_pos = vec_plus(new_pos, *dir);
                    if !self.is_valid_move(block_new_pos) {
                        continue;
                    }
                    new_brd[block_new_pos.0 as usize][block_new_pos.1 as usize] = 'X';
                }
                if self.targets.contains(&(pos.0, pos.1)) {
                    new_brd[pos.0 as usize][pos.1 as usize] = '*';
                } else {
                    new_brd[pos.0 as usize][pos.1 as usize] = '.';
                }
                new_brd[new_pos.0 as usize][new_pos.1 as usize] = '@';
                children.push(Board::new(new_brd, self.targets.clone()));
            }
        }
        children
    }

    fn find_OoIs(&self) -> (Vector, Vectors) {
        let mut boxes = vec![];
        let mut robot_pos = (0, 0);

        for i in 0..self.brd.len() {
            for j in 0..self.brd[0].len() {
                if self.brd[i][j] == '@' {
                    robot_pos = (i as i16, j as i16);
                } else if self.brd[i][j] == 'X' {
                    boxes.push((i as i16, j as i16));
                }
            }
        }
        (robot_pos, boxes)
    }

    fn solved(&self) -> bool {
        let (_, boxes) = self.find_OoIs();
        boxes.iter().all(|box_pos| self.targets.contains(box_pos))
    }
}

impl fmt::Display for Board {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let symbol_mapping: HashMap<char, char> = [
            ('.', '⬛'),
            ('#', '🟦'),
            (' ', '🟥'),
            ('X', '🟫'),
            ('@', '🚶'),
            ('*', '🎯'),
        ].iter().cloned().collect();

        for row in &self.brd {
            for &cell in row {
                write!(f, "{}", symbol_mapping.get(&cell).unwrap_or(&' '))?;
            }
            writeln!(f)?;
        }
        Ok(())
    }
}

fn soko_solver(board: Vec<&str>, limit: u16) -> Option<Vec<String>> {
    let board1: BaseBoard = board.iter().map(|row| row.chars().collect()).collect();

    let mut targets = vec![];
    for (i, row) in board.iter().enumerate() {
        for (j, cell) in row.chars().enumerate() {
            if cell == '*' {
                targets.push((i as i16, j as i16));
            }
        }
    }
    let board2 = Board::new(board1, targets);
    match dfbnb(board2, 0, limit){
        Some((res, _)) => {
            return Some(res)
        }
        None => {
            return None
        }
    }
}

fn dfbnb(board: Board, q: u16, U: u16) -> Option<(Vec<String>, u16)> {
    if q>=U {return None};

    if board.solved() {
        return Some((vec![board.to_string()], q));
    }

    let mut u_remembered = U;
    let mut out = None;
    for brd in board.find_children() {
        if let Some((mut soln, u)) = dfbnb(brd, q+1, u_remembered) {
            //if u>u_remembered {continue}
            soln.insert(0, board.to_string());
            out = Some((soln, u));
            u_remembered = u;
        }
    }
    out
}

fn main() {
    let boards = vec![
        vec![".@.", "#X.", "#*."],
        vec!["X#.", ".@#", "..*"],
        vec![
            "########",
            "#..#@.#.",
            "#....X.#",
            "#...#.X.",
            "#####**#",
            "    #.##",
            "    ####",
        ],
        vec![
            "#######",
            "#.....#",
            "#...@.#",
            "#.X.#.#",
            "#...#*#",
            "#######"
        ],
        vec![
            "########",
            "#..#@...",
            "#...#XX#",
            "#...#..#",
            "####*.*#",
            "   ##.##",
            "    ####",
        ]
    ];

    for board in boards {
        let board_len = board.len() as u16;
        if let Some(result) = soko_solver(board, board_len.pow(2)) {
            println!("Solution found:");
            for brd in result {
                println!("{}", brd);
            }
        } else {
            println!("No solution found.");
        }
    }
}
