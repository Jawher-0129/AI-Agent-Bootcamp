package com.optimized.paiementmanagement;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

/**
 * Main Application Class - Optimized Spring Boot Application
 * 
 * This application follows best practices:
 * - Constructor injection for all dependencies
 * - Interface-based service layer
 * - Proper exception handling
 * - Transaction management
 * - API documentation with OpenAPI
 * - Health monitoring with Actuator
 */
@SpringBootApplication
@EnableJpaAuditing
public class Application {
    
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
