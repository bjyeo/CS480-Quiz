-- Create index on endless_score if it doesn't exist
CREATE INDEX IF NOT EXISTS idx_users_endless_score ON public.users(endless_score DESC);

-- Create a view for the leaderboard
CREATE OR REPLACE VIEW public.leaderboard AS
SELECT 
    user_id,
    user_email,
    username,
    team_id,
    department,
    endless_score AS leaderboard_score,
    last_updated
FROM public.users
ORDER BY endless_score DESC;

-- Function to get a user's rank
CREATE OR REPLACE FUNCTION public.get_user_rank(p_user_email VARCHAR(255))
RETURNS INTEGER AS $$
SELECT rank
FROM (
    SELECT user_email, 
           RANK() OVER (ORDER BY endless_score DESC) as rank
    FROM public.users
) ranked
WHERE user_email = p_user_email;
$$ LANGUAGE SQL SECURITY DEFINER;

-- Function to get a user's department rank
CREATE OR REPLACE FUNCTION public.get_user_department_rank(p_user_email VARCHAR(255), p_department VARCHAR(100))
RETURNS INTEGER AS $$
SELECT rank
FROM (
    SELECT user_email, 
           RANK() OVER (PARTITION BY department ORDER BY endless_score DESC) as rank
    FROM public.users
    WHERE department = p_department
) ranked
WHERE user_email = p_user_email;
$$ LANGUAGE SQL SECURITY DEFINER;

-- Function to get a team's rank
CREATE OR REPLACE FUNCTION public.get_team_rank(p_team_id UUID)
RETURNS INTEGER AS $$
SELECT rank
FROM (
    SELECT team_id, 
           RANK() OVER (ORDER BY AVG(endless_score) DESC) as rank
    FROM public.users
    WHERE team_id IS NOT NULL
    GROUP BY team_id
) ranked
WHERE team_id = p_team_id;
$$ LANGUAGE SQL SECURITY DEFINER;

-- Function to update user's endless score
CREATE OR REPLACE FUNCTION public.update_endless_score(p_user_email VARCHAR(255), p_score INTEGER)
RETURNS VOID AS $$
BEGIN
    UPDATE public.users
    SET endless_score = p_score,
        last_updated = CURRENT_TIMESTAMP
    WHERE user_email = p_user_email;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;