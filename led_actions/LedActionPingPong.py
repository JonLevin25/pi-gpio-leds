from led_actions.LedAction import LedAction


class LedActionPingPong(LedAction):
    def get_norm_t_pingpong(self, t: float):
        norm_t_unclamped = (t - self.start_time) / self.iteration_time + self.norm_t_offset
        complete_iters = int(norm_t_unclamped)
        curr_ascending = self.start_ascending ^ complete_iters % 2  # true if currently ascending

        naive_norm_t = norm_t_unclamped % 1
        return naive_norm_t if curr_ascending else 1 - naive_norm_t