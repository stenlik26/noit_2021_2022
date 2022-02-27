export class SolutionInfo {
    code_ids: number = -1;
    solution_id: string = '';
    problem_name: string = '';
    num: number = -1;
    author_id: string = '';
    score: number = -1;
    author_name: string = '';

    constructor(
        code_ids: number,
        problem_name: string, 
        solution_id: string,
        author_id: string,
        author_name: string,
        score: number,
        num: number){
        this.code_ids = code_ids;
        this.problem_name = problem_name;
        this.solution_id = solution_id;
        this.num = num;
        this.author_id = author_id;
        this.score = score;
        this.author_name = author_name;
    }

    get_score(): string{
        if(this.score === -1){
            return '-';
        }
        else{
            return this.score.toString() + " / 10";
        }
    }

}