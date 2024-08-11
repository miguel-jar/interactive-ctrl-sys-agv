import tkinter as tk

class TrajectoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mapa de Trajetória")
        
        self.grid_size = 10  # Para exemplo, use uma matriz 10x10
        
        self.selected_points = []
        self.create_map()
        
    def create_map(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                btn = tk.Button(self.root, width=4, height=2,
                                command=lambda i=i, j=j: self.select_point(i, j))
                btn.grid(row=i, column=j)
                
    def select_point(self, x, y):
        self.selected_points.append((x, y))
        print(f"Ponto selecionado: ({x}, {y})")
        
        # Marque o ponto selecionado no mapa
        btn = tk.Button(self.root, width=4, height=2, bg="blue")
        btn.grid(row=x, column=y)
        
        # Desenhe a trajetória (opcional, aqui pode-se implementar uma função para desenhar linhas)
        
    def get_trajectory(self):
        return self.selected_points

if __name__ == "__main__":
    root = tk.Tk()
    app = TrajectoryApp(root)
    root.mainloop()
