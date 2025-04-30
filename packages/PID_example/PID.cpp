#include <cmath>  
#include <iostream>  
#include <thread>  
#include <chrono>  
  
// Alias per semplicità  
using real = double;  
  
// Struttura vettore 2 elementi  
struct Vector2 {  
    real v[2];  
};  
  
// Struttura matrice 2x2  
struct Matrix2x2 {  
    real m[2][2];  
};  
  
// Moltiplicazione matrice-vettore  
Vector2 mat_vec_mul(const Matrix2x2& M, const Vector2& v) {  
    Vector2 r;  
    r.v[0] = M.m[0][0]*v.v[0] + M.m[0][1]*v.v[1];  
    r.v[1] = M.m[1][0]*v.v[0] + M.m[1][1]*v.v[1];  
    return r;  
}  
  
// Somma vettori  
Vector2 vec_add(const Vector2& a, const Vector2& b) {  
    Vector2 r;  
    r.v[0] = a.v[0] + b.v[0];  
    r.v[1] = a.v[1] + b.v[1];  
    return r;  
}  
  
// Sottrazione vettori  
Vector2 vec_sub(const Vector2& a, const Vector2& b) {  
    Vector2 r;  
    r.v[0] = a.v[0] - b.v[0];  
    r.v[1] = a.v[1] - b.v[1];  
    return r;  
}  
  
// Moltiplicazione vettore per scalare  
Vector2 vec_scalar_mul(const Vector2& v, real s) {  
    Vector2 r;  
    r.v[0] = v.v[0] * s;  
    r.v[1] = v.v[1] * s;  
    return r;  
}  
  
// Stampa vettore  
void print_vector(const char* name, const Vector2& v) {  
    std::cout << name << ": [" << v.v[0] << ", " << v.v[1] << "]" << std::endl;  
}  
  
// Classe PID vettoriale  
class PID {  
public:  
    PID(real kp, real ki, real kd) : Kp(kp), Ki(ki), Kd(kd) {  
        integral = {0, 0};  
        prev_error = {0, 0};  
    }  
    Vector2 compute(const Vector2& error, real dt) {  
        integral = vec_add(integral, vec_scalar_mul(error, dt));  
        Vector2 derivative = vec_scalar_mul(vec_sub(error, prev_error), 1.0/dt);  
        Vector2 out = vec_add(  
            vec_add(vec_scalar_mul(error, Kp), vec_scalar_mul(integral, Ki)),  
            vec_scalar_mul(derivative, Kd)  
        );  
        prev_error = error;  
        return out;  
    }  
private:  
    real Kp, Ki, Kd;  
    Vector2 integral, prev_error;  
};  
  
int main() {  
    // Parametri iniziali  
    Vector2 input = {1.0, 2.0}; // Input costante  
    Matrix2x2 S = {{{1.0, 0.2}, {0.1, 0.9}}}; // Matrice di sensing  
    Vector2 O = {0.0, 0.0}; // Target  
    Matrix2x2 D = {{{0.8, 0.1}, {0.2, 0.7}}}; // Matrice di driving  
    real gain = 1.5;  
    PID pid(2.0, 0.5, 0.1); // Kp, Ki, Kd  
    real dt = 0.01; // 10 ms  
  
    // Loop di controllo PID  
    for (int step = 0; step < 10; ++step) {  
        // 1. Sensing: misura lo stato attuale  
        Vector2 sensed = mat_vec_mul(S, input);  
  
        // 2. Calcolo errore rispetto al target  
        Vector2 error = vec_sub(O, sensed);  
  
        // 3. Calcolo PID  
        Vector2 pid_out = pid.compute(error, dt);  
  
        // 4. Applica gain  
        Vector2 filtered = vec_scalar_mul(pid_out, gain);  
  
        // 5. Driving: calcola comando finale  
        Vector2 output = mat_vec_mul(D, filtered);  
  
        // 6. Stampa risultati di questa iterazione  
        std::cout << "Step " << step << std::endl;  
        print_vector("  Sensed", sensed);  
        print_vector("  Error", error);  
        print_vector("  PID output", pid_out);  
        print_vector("  Filtered", filtered);  
        print_vector("  Output", output);  
        std::cout << std::endl;  
  
        // 7. Attendi il prossimo ciclo (simula dt)  
        std::this_thread::sleep_for(std::chrono::milliseconds(10));  
    }  
    return 0;  
}  
