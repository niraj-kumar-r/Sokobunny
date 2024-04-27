use std::collections::HashMap;
use std::fmt;

type Vector = (i32, i32);
type BaseBoard = Vec<Vec<char>>;
type Vectors = Vec<Vector>;

fn vec_plus(v1: Vector, v2: Vector) -> Vector {
    (v1.0 + v2.0, v1.1 + v2.1)
}

struct Board {
    brd: BaseBoard,
    targets: Vectors,
}

impl fmt::Display for Board {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let symbol_mapping = [
            ('.', '⬛'),  // Empty space
            ('#', '🟦'),  // Wall
            ('X', '🟫'),  // Box
            ('@', '🚶'),  // Player
            ('*', '🎯')   // Target
        ].iter().cloned().collect::<HashMap<_, _>>();

        for row in &self.brd {
            for &cell in row {
                write!(f, "{}", symbol_mapping.get(&cell).unwrap_or(&' '))?;
            }
            writeln!(f)?;
        }
        Ok(())
    }
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
        x >= 0 && x < self.brd.len() as i32 && y >= 0 && y < self.brd[0].len() as i32 && self.brd[x as usize][y as usize] != '#'
    }

    fn find_children(&self) -> Vec<Board> {
        let DIRECTIONS = [('U', (0, -1)), ('D', (0, 1)), ('L', (-1, 0)), ('R', (1, 0))];
        let mut children = Vec::new();
        let (pos, _) = self.find_OoIs();
        for (_, dir) in DIRECTIONS.iter() {
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
                if self.targets.contains(&pos) {
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
        let mut boxes = Vec::new();
        let mut robot_pos = (0, 0);
        for (i, row) in self.brd.iter().enumerate() {
            for (j, &cell) in row.iter().enumerate() {
                if cell == '@' {
                    robot_pos = (i as i32, j as i32);
                } else if cell == 'X' {
                    boxes.push((i as i32, j as i32));
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

fn soko_solver(board: Vec<&str>) -> Option<Vec<String>> {
    let mut board1: BaseBoard = board.iter().map(|row| row.chars().collect()).collect();

    let mut targets = Vec::new();
    for (i, row) in board.iter().enumerate() {
        for (j, cell) in row.chars().enumerate() {
            if cell == '*' {
                targets.push((i as i32, j as i32));
            }
        }
    }
    let board2 = Board::new(board1, targets);
    DFBnB(board2, 16)
}

fn DFBnB(board: Board, u: usize) -> Option<Vec<String>> {
    if std::thread::current().stack().len() > u {
        return None;
    }
    if board.solved() {
        return Some(vec![board.to_string()]);
    }

    let mut out = None;
    for brd in board.find_children() {
        if let Some(soln) = DFBnB(brd, u) {
            let mut new_out = vec![board.to_string()];
            new_out.extend(soln);
            out = Some(new_out);
        }
    }

    out
}


fn main() -> (){
    
}
